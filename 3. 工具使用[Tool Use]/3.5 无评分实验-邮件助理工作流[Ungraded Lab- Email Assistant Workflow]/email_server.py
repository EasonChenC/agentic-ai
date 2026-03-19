"""
FastAPI Email Server - 模拟邮件服务
提供 REST API 接口用于邮件管理
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uvicorn

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ================================
# 数据库配置
# ================================
DATABASE_URL = "sqlite:///./emails.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ================================
# 数据库模型
# ================================
class EmailDB(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    recipient = Column(String, index=True)
    subject = Column(String)
    body = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)


# ================================
# Pydantic 模型
# ================================
class EmailCreate(BaseModel):
    recipient: str
    subject: str
    body: str


class EmailResponse(BaseModel):
    id: int
    sender: str
    recipient: str
    subject: str
    body: str
    timestamp: datetime
    read: bool

    class Config:
        from_attributes = True


# ================================
# FastAPI 应用
# ================================
app = FastAPI(title="Email Server API", version="1.0.0")

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================
# 数据库依赖
# ================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================================
# 初始化数据库
# ================================
def init_db():
    """创建数据库表"""
    Base.metadata.create_all(bind=engine)


def load_initial_emails(db: Session):
    """加载初始测试邮件"""
    # 检查是否已有数据
    if db.query(EmailDB).count() > 0:
        return

    initial_emails = [
        {
            "sender": "eric@work.com",
            "recipient": "you@email.com",
            "subject": "Happy Hour",
            "body": "We're planning drinks this Friday!",
            "timestamp": datetime(2025, 6, 13, 4, 48, 59),
            "read": False
        },
        {
            "sender": "boss@email.com",
            "recipient": "you@email.com",
            "subject": "Quarterly Report",
            "body": "Please send me the Q4 report by EOD.",
            "timestamp": datetime(2025, 6, 14, 9, 30, 0),
            "read": False
        },
        {
            "sender": "alice@work.com",
            "recipient": "you@email.com",
            "subject": "Project Update",
            "body": "The new feature is ready for review.",
            "timestamp": datetime(2025, 6, 14, 14, 15, 0),
            "read": False
        },
        {
            "sender": "hr@company.com",
            "recipient": "you@email.com",
            "subject": "Benefits Enrollment",
            "body": "Don't forget to complete your benefits enrollment.",
            "timestamp": datetime(2025, 6, 15, 10, 0, 0),
            "read": True
        },
    ]

    for email_data in initial_emails:
        email = EmailDB(**email_data)
        db.add(email)

    db.commit()


# ================================
# API 路由
# ================================

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    init_db()
    db = SessionLocal()
    try:
        load_initial_emails(db)
    finally:
        db.close()


@app.get("/")
async def root():
    """根路径"""
    return {"message": "Email Server API is running", "version": "1.0.0"}


@app.post("/send", response_model=EmailResponse)
async def send_email(email: EmailCreate):
    """发送新邮件"""
    db = SessionLocal()
    try:
        new_email = EmailDB(
            sender="you@email.com",  # 默认发件人
            recipient=email.recipient,
            subject=email.subject,
            body=email.body,
            timestamp=datetime.utcnow(),
            read=False
        )
        db.add(new_email)
        db.commit()
        db.refresh(new_email)
        return new_email
    finally:
        db.close()


@app.get("/emails", response_model=List[EmailResponse])
async def list_all_emails():
    """获取所有邮件（按时间倒序）"""
    db = SessionLocal()
    try:
        emails = db.query(EmailDB).order_by(EmailDB.timestamp.desc()).all()
        return emails
    finally:
        db.close()


@app.get("/emails/unread", response_model=List[EmailResponse])
async def list_unread_emails():
    """获取所有未读邮件"""
    db = SessionLocal()
    try:
        emails = db.query(EmailDB).filter(EmailDB.read == False).order_by(EmailDB.timestamp.desc()).all()
        return emails
    finally:
        db.close()


@app.get("/emails/search", response_model=List[EmailResponse])
async def search_emails(q: str = Query(..., description="搜索关键词")):
    """搜索邮件（在主题、正文、发件人中搜索）"""
    db = SessionLocal()
    try:
        emails = db.query(EmailDB).filter(
            (EmailDB.subject.contains(q)) |
            (EmailDB.body.contains(q)) |
            (EmailDB.sender.contains(q))
        ).order_by(EmailDB.timestamp.desc()).all()
        return emails
    finally:
        db.close()


@app.get("/emails/filter", response_model=List[EmailResponse])
async def filter_emails(
    recipient: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
):
    """按条件筛选邮件"""
    db = SessionLocal()
    try:
        query = db.query(EmailDB)

        if recipient:
            query = query.filter(EmailDB.recipient == recipient)

        if date_from:
            date_from_dt = datetime.fromisoformat(date_from)
            query = query.filter(EmailDB.timestamp >= date_from_dt)

        if date_to:
            date_to_dt = datetime.fromisoformat(date_to)
            query = query.filter(EmailDB.timestamp <= date_to_dt)

        emails = query.order_by(EmailDB.timestamp.desc()).all()
        return emails
    finally:
        db.close()


@app.get("/emails/{email_id}", response_model=EmailResponse)
async def get_email(email_id: int):
    """获取指定邮件"""
    db = SessionLocal()
    try:
        email = db.query(EmailDB).filter(EmailDB.id == email_id).first()
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        return email
    finally:
        db.close()


@app.patch("/emails/{email_id}/read", response_model=EmailResponse)
async def mark_email_as_read(email_id: int):
    """将邮件标记为已读"""
    db = SessionLocal()
    try:
        email = db.query(EmailDB).filter(EmailDB.id == email_id).first()
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")

        email.read = True
        db.commit()
        db.refresh(email)
        return email
    finally:
        db.close()


@app.patch("/emails/{email_id}/unread", response_model=EmailResponse)
async def mark_email_as_unread(email_id: int):
    """将邮件标记为未读"""
    db = SessionLocal()
    try:
        email = db.query(EmailDB).filter(EmailDB.id == email_id).first()
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")

        email.read = False
        db.commit()
        db.refresh(email)
        return email
    finally:
        db.close()


@app.delete("/emails/{email_id}")
async def delete_email(email_id: int):
    """删除邮件"""
    db = SessionLocal()
    try:
        email = db.query(EmailDB).filter(EmailDB.id == email_id).first()
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")

        db.delete(email)
        db.commit()
        return {"message": "Email deleted"}
    finally:
        db.close()


@app.get("/reset_database")
async def reset_database():
    """重置数据库到初始状态"""
    db = SessionLocal()
    try:
        # 删除所有邮件
        db.query(EmailDB).delete()
        db.commit()

        # 重新加载初始邮件
        load_initial_emails(db)

        return {"message": "Database reset and emails reloaded"}
    finally:
        db.close()


# ================================
# 主函数
# ================================
if __name__ == "__main__":
    print("Starting Email Server on http://127.0.0.1:5002")
    print("API Documentation: http://127.0.0.1:5002/docs")
    uvicorn.run(app, host="127.0.0.1", port=5002)
