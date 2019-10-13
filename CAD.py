__window__.Visible = False
import clr
import System
clr.AddReference("System.Core")
from System.Collections.Generic import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
doc = __revit__.ActiveUIDocument.Document
collector = FilteredElementCollector(doc).OfClass(ImportInstance).ToElements()
try:
	lista=[]
	fajlovi=[]
	for item in collector:
		params=list(item.Parameters)
		for i in params:
			if i.Definition.Name=="Name" and (".dwg" in i.AsString() or ".DWG" in i.AsString()):
				#print(i.AsString()+" "+item.Id.ToString())
				lista.append(item.Id)
				fajlovi.append(item)

	col=List[ElementId](lista)

	for f in fajlovi:
		if f.IsHidden(doc.ActiveView)==True:
			t = Transaction(doc, 'Unhide CAD files')
			t.Start()
			doc.ActiveView.UnhideElements(col)
			t.Commit()
		else:
			t = Transaction(doc, 'Hide CAD files')
			t.Start()
			doc.ActiveView.HideElements(col)
			t.Commit() 
except Exception:
	TaskDialog.Show("Missing CAD", "No CAD/DWG files loaded")

