# Nft Rarity

Like art - Not all NFTs are created equally.

NFT Rarity is a repository for querying a collection on opensea, running a rarity algorithim on the collection, and inserting it into a mongo db instance.

With this you can query the collection against your database instance to see the rarity of an NFT.

Pull requests on improving the algorithim are welcome.

## Getting Started

You will require an opensea API key as well as a MongoDB instance

Set `main_collection_name` in the python script as the collection you want to query

copy `.env.example` to `.env` and set the appropriate keys

run `python3 scripts/rarity.py`
