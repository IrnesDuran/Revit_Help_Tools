__window__.Visible = False
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory,Transaction
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI import UIApplication
doc = __revit__.ActiveUIDocument.Document                      
collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RasterImages).ToElements()
coll = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RasterImages).ToElementIds()
try:
	catId=collector[0].Category.Id
	if collector[0].IsHidden(doc.ActiveView)==True:
		t = Transaction(doc, 'Unhide Raster Image files')
		t.Start()
		doc.ActiveView.UnhideElements(coll)
		t.Commit()
	else:
		t = Transaction(doc, 'Hide Raster Image files')
		t.Start()
		doc.ActiveView.HideElements(coll)
		t.Commit()
except Exception:
	TaskDialog.Show("Missing Raster Image", "No Raster Image files loaded")
