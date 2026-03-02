from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bank_name = Column(String, nullable=False)
    account_number = Column(String, nullable=False)

    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Account(bank_name='{self.bank_name}', account_number='{self.account_number}')>"


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False) # 'debit' or 'credit'
    category = Column(String, nullable=True) # E.g., 'Food', 'Shopping', etc.
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)

    account = relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(date='{self.date}', description='{self.description[:15]}...', amount={self.amount}, type='{self.type}', category='{self.category}')>"
