from openerp.osv import osv, fields
from tempfile import TemporaryFile
import csv

class ExtendedInventoryReport(osv.osv_memory):
    _name = 'extended.inventory.report'


    def run_realtime_report(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0])
	out = TemporaryFile('w+b')
	fieldnames = ['SKU', 'NAME', 'COST', 'QTY', 'VALUE']
        writer = csv.DictWriter(out, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()

	product_obj = self.pool.get('product.product')
	products = product_obj.search(cr, uid, [])
	res = []
	totals = []
	for product in product_obj.browse(cr, uid, products):
	    qty_available = product.qty_available
	    if qty_available > 0:
		res.append({'SKU': product.default_code,
			    'NAME': product.name,
			    'COST': product.standard_price,
			    'QTY': qty_available,
			    'VALUE': round(qty_available, 2) * round(product.standard_price, 2),
		})
		totals.append(round(qty_available, 2) * round(product.standard_price, 2))


	for row in res:
	    writer.writerow(row)
	writer.writerow({})
	writer.writerow({})
	writer.writerow({'QTY': 'TOTAL VALUE', 'VALUE': round(sum(totals), 2)})

        return self.pool.get('pop.up.file').open_output_file(cr, uid, 'inventory.csv', out, \
		'Inventory Report', context=context)
