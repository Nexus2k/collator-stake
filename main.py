from operator import itemgetter
from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

substrate = SubstrateInterface(
    url="wss://rpc-0.zeitgeist.pm"
)
collator_size = substrate.query(
    module='ParachainStaking',
    storage_function='TotalSelected'
)
collators = substrate.query(
    module='ParachainStaking',
    storage_function='CandidatePool'
)
chain_symbol = str(substrate.get_constant('Currency','GetNativeCurrencyId')).upper()
chain_decimals = substrate.token_decimals

print("%s Collator stats:" % (substrate.name))
print("=========================")
collator_set = []
for collator in collators:
    amount = float(collator["amount"]) / 10**chain_decimals
    collator_set.append({"amount": amount,"owner": collator["owner"]})
count = 0
for collator in sorted(collator_set,key=itemgetter('amount'),reverse=True):
    print("%.0f %s delegated to %s" % (collator['amount'], chain_symbol, collator['owner']))
    count += 1
    if count == collator_size:
        print("----- (Outside of selected collators) -----")