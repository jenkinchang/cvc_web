from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, date
from typing import Optional, List, Dict

from pydantic import condecimal, validator
from sqlmodel import SQLModel, Field, Relationship


class AccountRole(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: Optional[str] = Field(default=None)

    father_id: Optional[int] = Field(foreign_key="accountrole.id")
    father: Optional["AccountRole"] = Relationship(
        back_populates="childs",
        sa_relationship_kwargs={"remote_side": "AccountRole.id"},
    )
    childs: List["AccountRole"] = Relationship(back_populates="father")

    accounts: List["Account"] = Relationship(back_populates="role")

    @property
    def tree(self) -> Dict[str, int | str | List[Dict]]:
        return {
            "id": self.id,
            "label": self.name,
            "children": [child.tree for child in self.childs] if self.childs else [],
        }


class BankAccount(SQLModel, table=True):
    """
    银行账户

    id: int
    name: str

    bank_account_num: str  # 银行账号
    bank_account_name: str  # 银行户名
    bank: str  # 开户行全称
    bank_short: str  # 开户行简称

    account: Account  # 结算人

    flows_out: List["MoneyFlow"]  # 付款流水
    flows_in: List["MoneyFlow"]  # 收款流水
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    bank_account_num: Optional[str]  # 银行账号
    bank_account_name: Optional[str]  # 银行户名
    bank: Optional[str]  # 开户行全称
    bank_short: Optional[str]  # 开户行简称

    account_id: Optional[str] = Field(foreign_key="account.id")
    account: Optional["Account"] = Relationship(back_populates="bank_accounts")

    flows_out: List["MoneyFlow"] = Relationship(
        back_populates="bank_account_out",
        sa_relationship_kwargs={"foreign_keys": "MoneyFlow.bank_account_out_id"},
    )
    flows_in: List["MoneyFlow"] = Relationship(
        back_populates="bank_account_in",
        sa_relationship_kwargs={"foreign_keys": "MoneyFlow.bank_account_in_id"},
    )


class Account(SQLModel, table=True):
    """
    结算人

    id: int
    name: str

    role: AccountRole

    bank_accounts: List[BankAccount]
    bill_details: List[MoneyBillDetail]
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    role_id: Optional[int] = Field(foreign_key="accountrole.id")
    role: Optional["AccountRole"] = Relationship(back_populates="accounts")

    bank_accounts: List[BankAccount] = Relationship(back_populates="account")
    bill_details: List["MoneyBillDetail"] = Relationship(back_populates="account")


class MoneyFlowDetail(SQLModel, table=True):
    """
    细分流水

    id: Optional[int]
    name: Optional[str]

    amount: Decimal = 0  # 细分交易额

    # 关联实际流水
    money_flow: Optional["MoneyFlow"]

    # 关联账单
    bill: Optional["MoneyBill"]
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    # 细分交易额
    amount: condecimal(max_digits=16, decimal_places=2) = Field(default=0)

    # 关联实际流水
    money_flow_id: Optional[int] = Field(foreign_key="moneyflow.id")
    money_flow: Optional["MoneyFlow"] = Relationship(back_populates="flow_details")

    # 关联账单
    bill_id: Optional[int] = Field(foreign_key="moneybill.id")
    bill: Optional["MoneyBill"] = Relationship(back_populates="flow_details")

    @validator("amount", pre=True, always=True)
    def amount_validator(cls, value):
        """
        金额设为两位小数且检测是否大于0
        """
        if isinstance(value, (float, int)):
            if value < Decimal("0.0"):
                raise ValueError("Amount must be greater than or equal to 0")
            return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return value


# 财务基本表
class MoneyFlow(SQLModel, table=True):
    """
    实际流水

    id: Optional[int]
    name: Optional[str]

    time: Optional[datetime]  # 交易时间
    msg_public: Optional[str]  # 银行摘要
    msg_bank: Optional[str]  # 银行用途
    msg_inside: Optional[str]  # 内部备注
    bank_flow_id: Optional[str]  # 银行流水号

    amount: condecimal | int | float  # 交易额

    # 关联银行账号
    bank_account_out: Optional[BankAccount]
    bank_account_in: Optional[BankAccount]

    # 关联细分流水
    flow_details: List["MoneyFlowDetail"]
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    time: Optional[datetime] = Field(default=None)  # 交易时间
    msg_public: Optional[str] = Field(default=None)  # 银行摘要
    msg_bank: Optional[str] = Field(default=None)  # 银行用途
    msg_inside: Optional[str] = Field(default=None)  # 内部备注
    bank_flow_id: Optional[str] = Field(default=None)  # 银行流水号

    # 实际交易额
    amount: condecimal(max_digits=16, decimal_places=2) = Field(default=0)

    # 关联银行账号
    bank_account_out_id: Optional[str] = Field(
        default=None, foreign_key="bankaccount.id"
    )
    bank_account_in_id: Optional[str] = Field(
        default=None, foreign_key="bankaccount.id"
    )
    bank_account_out: Optional[BankAccount] = Relationship(
        back_populates="flows_out",
        sa_relationship_kwargs={"foreign_keys": "MoneyFlow.bank_account_out_id"},
    )
    bank_account_in: Optional[BankAccount] = Relationship(
        back_populates="flows_in",
        sa_relationship_kwargs={"foreign_keys": "MoneyFlow.bank_account_in_id"},
    )

    # 关联细分流水
    flow_details: List["MoneyFlowDetail"] = Relationship(back_populates="money_flow")

    @validator("amount", pre=True, always=True)
    def amount_validator(cls, value):
        """
        金额设为两位小数且检测是否大于0
        """
        if isinstance(value, (float, int)):
            if value < Decimal("0.0"):
                raise ValueError("Amount must be greater than or equal to 0")
            return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return value


class MoneyBillDetail(SQLModel, table=True):
    """
    各方应结表

    id: int
    name: str

    # 关联结算人
    account: Account
    # 关联结算单
    bill: MoneyBill
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    amount: condecimal(max_digits=16, decimal_places=2) = Field(default=0)

    # 关联结算人
    account_id: Optional[str] = Field(default=None, foreign_key="account.id")
    account: Optional[Account] = Relationship(back_populates="bill_details")
    # 关联结算单
    bill_id: Optional[str] = Field(default=None, foreign_key="moneybill.id")
    bill: Optional["MoneyBill"] = Relationship(back_populates="bill_details")

    @validator("amount", pre=True, always=True)
    def amount_validator(cls, value):
        """
        金额设为两位小数且检测是否大于0
        """
        if isinstance(value, (float, int)):
            return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return value


class MoneyBill(SQLModel, table=True):
    """
    结算单

    id: int
    name: str

    type: str
    month_period: date

    # 关联细分流水
    flow_details: List["MoneyFlowDetail"]
    # 关联各方应结表
    bill_details: List["MoneyBillDetail"]
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    type: str
    month_period: Optional[date] = Field(default=None)

    # 关联细分流水
    flow_details: List["MoneyFlowDetail"] = Relationship(back_populates="bill")
    # 关联各方应结表
    bill_details: List["MoneyBillDetail"] = Relationship(back_populates="bill")


def main():
    pass


if __name__ == "__main__":
    main()
