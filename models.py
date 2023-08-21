from decimal import Decimal
from datetime import datetime, date
from typing import Optional, List, Dict
from pydantic import condecimal
from sqlmodel import SQLModel, Field, Relationship


class BankAccountRole(SQLModel, table=True):
    __tablename__ = "bank_account_role"
    id: Optional[int] = Field(primary_key=True)
    name: str

    father_id: Optional[int] = Field(foreign_key="bank_account_role.id")
    father: Optional["BankAccountRole"] = Relationship(
        back_populates="childs",
        sa_relationship_kwargs={"remote_side": "BankAccountRole.id"},
    )
    childs: List["BankAccountRole"] = Relationship(back_populates="father")

    bank_account: List["BankAccount"] = Relationship(back_populates="role")

    @property
    def tree(self) -> Dict[str, int | str | List[Dict]]:
        return {
            "id": self.id,
            "label": self.name,
            "children": [child.tree for child in self.childs] if self.childs else [],
        }


class BankAccount(SQLModel, table=True):
    __tablename__ = "bankAccount"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)

    account_id: Optional[str]
    account_name: Optional[str]
    bank: Optional[str]
    bank_short: Optional[str]

    flow: List["MoneyFlow"] = Relationship(back_populates="account")
    role_id: Optional[int] = Field(foreign_key="bank_account_role.id")
    role: BankAccountRole = Relationship(back_populates="bank_account")


# 财务基本表
class MoneyFlow(SQLModel, table=True):
    """
    实际流水

    记录方

    现金流水证明

    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    account_id: Optional[str] = Field(default=None, foreign_key="bankAccount.id")  # 我方账号: str
    account: Optional[BankAccount] = Relationship(back_populates="flow")  # 我方账号: BankAccount
    con_account_id: Optional[str] = Field(default=None, foreign_key="bankAccount.id")  # 对方账号: str
    con_account: Optional[BankAccount] = Relationship(back_populates="flow")  # 对方账号: BankAccount

    outcome: condecimal(max_digits=16, decimal_places=2) = Field(default=0)  # 收入
    income: condecimal(max_digits=16, decimal_places=2) = Field(default=0)  # 支出
    balance: condecimal(max_digits=16, decimal_places=2) = Field(default=0)  # 余额

    time: Optional[datetime] = Field(default=None)  # 交易时间
    msg_public: Optional[str] = Field(default=None)  # 银行摘要
    msg_bank: Optional[str] = Field(default=None)  # 银行用途
    msg_inside: Optional[str] = Field(default=None)  # 内部备注
    bank_flow_id: Optional[str] = Field(default=None)  # 银行流水号

    details: List["MoneyDetail"] = Relationship(back_populates="flow")

    @property
    def details_sum(self) -> Decimal:
        # 凭证收支
        outcome = sum([detail.outcome for detail in self.details])
        income = sum([detail.income for detail in self.details])
        return outcome - income  # Decimal类型检查过了

    @property
    def unknow_flow(self) -> Decimal:
        # 不明收支
        return self.income - self.outcome - self.details_sum

    @property
    def detail_state(self) -> str:
        # 凭证状态
        if not self.details:
            return "无凭证"
        elif self.unknow_flow != Decimal(0):
            return "不明收支"
        else:
            return "-"


class MoneyBill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    month_period: Optional[date] = Field(default=None)

    details: List["MoneyDetail"] = Relationship(back_populates="bill")


class MoneyDetail(SQLModel, table=True):
    """
    不明流水
    流水状态
    入单状态
    流水日期
    收支
    内部备注
    商单达人
    金额&备注
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    class_1: Optional[str] = Field(default=None)
    class_2: Optional[str] = Field(default=None)
    outcome: condecimal(max_digits=16, decimal_places=2) = Field(default=0)
    income: condecimal(max_digits=16, decimal_places=2) = Field(default=0)
    month_period: Optional[date] = Field(default=None)  # 账期
    msg_inside: Optional[str] = Field(default=None)  # 内部备注

    flow_id: Optional[str] = Field(default=None)
    flow: MoneyFlow = Relationship(back_populates="details")
    bill_id: Optional[str] = Field(default=None)
    bill: MoneyBill = Relationship(back_populates="details")


def main():
    pass


if __name__ == "__main__":
    main()
