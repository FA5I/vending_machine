init --1p=100 --2p=100 --5p=100 --10p=100 --20p=100 --50p=100 --100p=100 --200p=100 

display_balances

select_product --product=A1

insert_coins --1p=100 --2p=1 --5p=1 --10p=1 --20p=1 --50p=1 --100p=1 --200p=1
 
 display_machine_state

 get_change

 pytest ./src/tests/tests.py

 pipenv install --editable .