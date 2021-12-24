from pyteal import *
from decouple import config

# default values
manager_addr = Addr( config( "MANAGER_ADDR" ) )
emp1_addr = Addr( config( "EMP1_ADDR" ) )
emp2_addr = Addr( config( "EMP2_ADDR" ) )

salary1 = Int( 3000 )
salary2 = Int( 4000 )

fee_limit = Int( 10000 )
time_period = Int( 1 )
duration = Int( 1 )
timeout = Int( 12 )
lease = Bytes( "base64" , "023sdDE2" )

def payroll(
  manager_addr = manager_addr , emp1_addr = emp1_addr , emp2_addr = emp2_addr ,
  salary1 = salary1 , salary2 = salary2 , fee_limit = fee_limit , time_period = time_period ,
  duration = duration , timeout = timeout , lease = lease
):
  pay_salary_core = And(
    Txn.type_enum() == TxnType.Payment ,
    # or
    # Txn.type_enum() == Int( 1 ) ,
    Txn.fee() < fee_limit ,
    Txn.first_valid() % time_period == Int( 0 ) ,
    Txn.last_valid() == duration + Txn.first_valid() ,
    Txn.lease() == lease
  )

  pay_salary_transfer = And(
    Gtxn[ 0 ].sender() == Gtxn[ 1 ].sender() ,
    Txn.close_remainder_to() == Global.zero_address() ,
    Gtxn[ 0 ].receiver() == emp1_addr ,
    Gtxn[ 1 ].receiver() == emp2_addr ,
    Gtxn[ 0 ].amount() == salary1 ,
    Gtxn[ 1 ].amount() == salary2
  )

  pay_salary_close = And(
    Txn.close_remainder_to() == manager_addr ,
    Txn.rekey_to() == Global.zero_address() ,
    Txn.receiver() == Global.zero_address() ,
    Txn.first_valid() == timeout ,
    Txn.amount() == Int( 0 )
  )

  pay_salary_escrow = pay_salary_core.And( pay_salary_transfer.Or( pay_salary_close ) )

  return pay_salary_escrow

if __name__ == "__main__":
  with open( "tealCode/paySalary.teal" , "w" ) as f:
    compiled = compileTeal( payroll() , Mode.Signature , version = 5 )
    f.write( compiled )