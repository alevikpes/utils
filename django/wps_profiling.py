import cProfile
import pstats


# read profile and configure the output
p = pstats.Stats('/app/src/wps.prof')
p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats('cumulative').print_stats(10)
