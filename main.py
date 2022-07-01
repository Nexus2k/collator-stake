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

print("Zeitgeist Collator stats:")
print("=========================")
collator_set = []
for collator in collators:
    amount = float(collator["amount"]) / 1e10
    collator_set.append({"amount": amount,"owner": collator["owner"]})
count = 0
for collator in sorted(collator_set,key=itemgetter('amount'),reverse=True):
    print("%.0f ZTG delegated to %s" % (collator['amount'], collator['owner']))
    count += 1
    if count == collator_size:
        print("----- (Outside of selected collators) -----")