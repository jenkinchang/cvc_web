from decimal import Decimal
from datetime import datetime, date
from typing import Optional, List, Dict
from pydantic import condecimal
from sqlmodel import SQLModel, Field, Relationship


class AccountRole(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str

    father_id: Optional[int] = Field(foreign_key="accountrole.id")
    father: Optional["AccountRole"] = Relationship(
        back_populates="childs",
        sa_relationship_kwargs={"remote_side": "BankAccountRole.id"},
    )
    childs: List["AccountRole"] = Relationship(back_populates="father")

    accounts: List["BankAccount"] = Relationship(back_populates="role")


#
#     @property
#     def tree(self) -> Dict[str, int | str | List[Dict]]:
#         return {
#             "id": self.id,
#             "label": self.name,
#             "children": [child.tree for child in self.childs] if self.childs else [],
#         }


class BankAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)

    bank_account_num: Optional[str]  # 银行账号
    bank_account_name: Optional[str]  # 银行户名
    bank: Optional[str]  # 开户行全称
    bank_short: Optional[str]  # 开户行简称

    # role_id: Optional[int] = Field(foreign_key="bank_account_role.id")
    # role: BankAccountRole = Relationship(back_populates="bank_account")

    account_id: Optional[int] = Field(foreign_key="account.id")
    account: Optional["Account"] = Relationship(back_populates="bank_accounts")

    flows_out: List["MoneyFlow"] = Relationship(back_populates="bank_account_out")
    flows_in: List["MoneyFlow"] = Relationship(back_populates="bank_account_in")


class Account(SQLModel, table=True):
    """
    结算人
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)

    role_id: Optional[int] = Field(foreign_key="accountrole.id")
    role: Optional["AccountRole"] = Relationship(back_populates="accounts")

    bank_accounts: List[BankAccount] = Relationship(back_populates="account")
    bill_details: List["MoneyBillDetail"] = Relationship(back_populates="account")


class MoneyFlowDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    # 关联实际流水
    money_flow_id: Optional[int] = Field(foreign_key="moneyflow.id")
    money_flow: Optional["MoneyFlow"] = Relationship(back_populates="flow_details")

    # 关联账单
    bill_id: Optional[int] = Field(foreign_key="moneybill.id")
    bill: Optional["MoneyBill"] = Relationship(back_populates="flow_details")


# 财务基本表
class MoneyFlow(SQLModel, table=True):
    """
    实际流水

    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    time: Optional[datetime] = Field(default=None)  # 交易时间
    msg_public: Optional[str] = Field(default=None)  # 银行摘要
    msg_bank: Optional[str] = Field(default=None)  # 银行用途
    msg_inside: Optional[str] = Field(default=None)  # 内部备注
    bank_flow_id: Optional[str] = Field(default=None)  # 银行流水号

    amount: condecimal(max_digits=16, decimal_places=2) = Field(default=0)  # 交易额

    # 关联银行账号
    bank_account_out_id: Optional[str] = Field(default=None, foreign_key="bankaccount.id")
    bank_account_in_id: Optional[str] = Field(default=None, foreign_key="bankaccount.id")
    bank_account_out: Optional[BankAccount] = Relationship(back_populates="flows_out")
    bank_account_in: Optional[BankAccount] = Relationship(back_populates="flows_in")

    # 关联细分流水
    flow_details: List["MoneyFlowDetail"] = Relationship(back_populates="money_flow")

    # @property
    # def details_sum(self) -> Decimal:
    #     # 凭证收支
    #
    # @property
    # def unknow_flow(self) -> Decimal:
    #
    # @property
    # def detail_state(self) -> str:
    #     # 凭证状态


class MoneyBillDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    # 关联结算人
    account_id: Optional[str] = Field(default=None, foreign_key="account.id")
    account: Optional[Account] = Relationship(back_populates="bill_details")
    # 关联结算单
    bill_id: Optional[str] = Field(default=None, foreign_key="moneybill.id")
    bill: Optional["MoneyBill"] = Relationship(back_populates="bill_details")


class MoneyBill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    type: str
    month_period: Optional[date] = Field(default=None)

    # 关联细分流水
    flow_details: List["MoneyFlowDetail"] = Relationship(back_populates="bill")
    # 关联各方应结表
    bill_details: List["MoneyBillDetail"] = Relationship(back_populates="bill")


# class MoneyDetail(SQLModel, table=True):
#     """
#     不明流水
#     流水状态
#     入单状态
#     流水日期
#     收支
#     内部备注
#     商单达人
#     金额&备注
#     """
#
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: Optional[str] = Field(default=None)
#
#     class_1: Optional[str] = Field(default=None)
#     class_2: Optional[str] = Field(default=None)
#     outcome: condecimal(max_digits=16, decimal_places=2) = Field(default=0)
#     income: condecimal(max_digits=16, decimal_places=2) = Field(default=0)
#     month_period: Optional[date] = Field(default=None)  # 账期
#     msg_inside: Optional[str] = Field(default=None)  # 内部备注
#
#     flow_id: Optional[str] = Field(default=None)
#     flow: MoneyFlow = Relationship(back_populates="details")
#     bill_id: Optional[str] = Field(default=None)
#     bill: MoneyBill = Relationship(back_populates="details")


def main():
    pass


if __name__ == "__main__":
    main()
