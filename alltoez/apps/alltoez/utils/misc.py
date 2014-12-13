def uniqify(seq, idfun=None):
	# Order preserving uniqify method to return a unique list of values
	if idfun is None:
		def idfun(x): return x
	seen = {}
	result = []
	for item in seq:
		marker = idfun(item)
		if marker in seen: continue
		seen[marker] = 1
		result.append(item)
	return result

def monthdelta(date, delta):
	"""
	Enables you to subtract or add a month to the date provided.
	e.g. monthdelta(datetime.now(), -1)
	"""
	m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
	if not m: m = 12
	d = min(date.day, [31,
		29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
	return date.replace(day=d,month=m, year=y)