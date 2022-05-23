def _getAlgo(documents, _filter):
   return [d for d in documents if sum(1 for k, v in d.items() if _filter.get(k)==v) >= len(_filter)]