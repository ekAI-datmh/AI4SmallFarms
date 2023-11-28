# https://github.com/spgriffin/polis

from collections import Counter
from shapely import geometry
from rtree import index
from base import Base


class Polis(Base):
    def __init__(self):
        super().__init__()

    def compare_polys(self, poly_a, poly_b):
        boundary_a, boundary_b = poly_a.exterior, poly_b.exterior
        dist = self.polis(boundary_a.coords, boundary_b)
        dist += self.polis(boundary_b.coords, boundary_a)
        return dist

    @staticmethod
    def polis(coords, boundary):
        summ = 0.0
        for pt in (geometry.Point(c) for c in coords[:-1]):
            summ += boundary.distance(pt)
        return summ / float(2 * len(coords))

    def score(self, reference_gdf, vector_gdf):
        ref_polys = reference_gdf['geometry'].to_list()
        idx = index.Index((i, geom.bounds, None) for i, geom in enumerate(ref_polys))

        hits = []
        vector_gdf['polis'] = None
        for index_, row_ in vector_gdf.iterrows():
            row_geom = vector_gdf.loc[index_, 'geometry']
            ref_pindices = [i for i in idx.nearest(row_geom.bounds)]
            if len(ref_pindices) > 5:
                ref_pindices = ref_pindices[:5]
            scores = [self.compare_polys(row_geom, ref_polys[i]) for i in ref_pindices]
            polis_score = min(scores)
            hits.append(ref_pindices[scores.index(polis_score)])
            vector_gdf.loc[index_, 'polis'] = polis_score

        print("Number of matches: {}".format(len(hits)))
        print("Number of misses: {}".format(len(ref_polys) - len(hits)))
        print("Duplicate matches: {}".format(sum([1 for i in Counter(hits).values() if i > 1])))

        return vector_gdf
