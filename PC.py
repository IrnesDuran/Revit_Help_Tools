__window__.Visible = False
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory,Transaction
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI import UIApplication
doc = __revit__.ActiveUIDocument.Document                      
collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PointClouds).ToElements()
coll = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PointClouds).ToElementIds()
try:
	catId=collector[0].Category.Id
	if collector[0].IsHidden(doc.ActiveView)==True:
		t = Transaction(doc, 'Unhide Point Cloud files')
		t.Start()
		doc.ActiveView.UnhideElements(coll)
		t.Commit()
	else:
		t = Transaction(doc, 'Hide Point Cloud files')
		t.Start()
		doc.ActiveView.HideElements(coll)
		t.Commit()
except Exception:
	TaskDialog.Show("Missing Point Cloud", "No Point Cloud files loaded")
