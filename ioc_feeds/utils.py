from .models import Ioc, Stats

# checks if an ioc is already added to the database!
def is_added(ioc):
    return Ioc.objects.filter(ioc=ioc['ioc']).exists()

# adds an ioc to the database
def add(ioc):
    try:
        # transform the singular source into an array of sources!
        sources = []
        sources.append(ioc["source"])
        # Adding it to the database!
        Ioc.objects.create(
            ioc=ioc["ioc"],
            type=ioc["type"],
            sources=sources
        )
        # adding to new_ioc_count from stats table
        stats, created = Stats.objects.get_or_create(pk=1)
        stats.new_iocs_count += 1
        stats.save()
    except Exception as e:
        print(e)

# updates the ioc!
# if an ioc is in 2 or more feeds append the new source!
# increase the frequency
def update(ioc):
    print(f"Updating Ioc: {ioc['ioc']}")
    try:
        gotten_ioc = Ioc.objects.get(ioc=ioc["ioc"])
        # if source is not in the list of sources add it!
        if ioc["source"] not in gotten_ioc.sources:
            gotten_ioc.sources.append(ioc["source"])
        gotten_ioc.frequency += 1
        gotten_ioc.save()
        stats, created = Stats.objects.get_or_create(pk=1)
        stats.frequent_iocs_count += 1
        stats.save()
    except Ioc.DoesNotExist as e:
        print(f"An error occurred {e}")