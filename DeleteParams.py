__window__.Visible = False
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System.Windows.Forms import Application, Form, StatusBar,Button,ToolTip
from System.Windows.Forms import ListBox, DockStyle, SelectionMode, AnchorStyles
from System.Windows.Forms import ListView, View, ColumnHeader
from System.Windows.Forms import ListViewItem, DockStyle, SortOrder,CheckBox
from System.Drawing import Size
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory,Transaction
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI import UIApplication
doc = __revit__.ActiveUIDocument.Document                       # document instance loaded
if doc.IsFamilyDocument==False:                                 # catch exception on not being in family editor
   TaskDialog.Show("Not in family editor", "Please enter family editor mode")
   quit()
 
  
mgr = doc.FamilyManager;                                        # family editor loaded
fps = mgr.Parameters;                                           # FamilyParameterSet loaded
paramsList=list(fps)                                            # cast FamilyParameterSet to Python list
editableParams = []                                             # created list to add parameter which are non Built-in (therefore can be removed)
for bip in fps:
   if bip.Definition.BuiltInParameter.ToString()=="INVALID":
       editableParams.append(bip)
                      
senderlist =[]                                                  # created list which will be appended by checkboxes from Listview
 
class IForm(Form):                                              # Windows Form created (inherits from Form)                            
 
   def __init__(self):
       self.Text = 'Select multiple parameters for deletion'
     
       button = Button()                                       # Button created
       button.Text = "Delete Parameters"                       # with this name
       button.Dock = DockStyle.Bottom                          # it is docked to bottom of the form
       button.Click += self.OnClick                            # CLick event is rissent and uses OnClick function
       self.Controls.Add(button)                               # this control adds button
 
 
       name = ColumnHeader()                                   # these 3 are column header names for 3 parameter properties I am going to use. -1 means longest value will be used for length
       name.Text = 'Parameter'
       name.Width = -1
       paramgr = ColumnHeader()
       paramgr.Text = 'Parameter Group'
       paramgr.Width = -1
       parfor = ColumnHeader()
       parfor.Text = 'Parameter Formula'
       parfor.Width = 140
     
 
       self.SuspendLayout()                                        # not sure if this must be used, but it works                     
 
       lv = ListView()                                             # this makes a Listview
       lv.Parent = self                                          
       lv.FullRowSelect = False
       lv.CheckBoxes=True
       lv.GridLines = True
       lv.AllowColumnReorder = True
       lv.View = View.Details
       lv.Columns.AddRange((name, paramgr,parfor))                 # columns have been created for column headers above
       lv.ColumnClick += self.OnColumnClick                        # ColumnCLick event enables sorting from OnColumnClick function
  
 
       for par in paramsList:                                      # this adds parameter properties to listview columns asn subitems
           item = ListViewItem()
           item.Text = par.Definition.Name                         # first item is parameter name
           item.SubItems.Add(par.Definition.ParameterGroup.ToString()) # second is parameter group to string
           if par.Formula:                                         # if formula exists at all
               item.SubItems.Add(par.Formula.ToString())           # show it as string
           else:                                                   # if it does not exist
               item.SubItems.Add("-")                              # add anything
           lv.Items.Add(item)                                      # add item to ListViewItems
      
 
       lv.Dock = DockStyle.Fill                                    # fill in Form with this lisview (buttin is docked to bottom as seen above)
       lv.ItemCheck += self.OnSelected                             # ItemCheck event is called with OnSelected function
      
       self.ResumeLayout()                                         # not sure if this must be used, but it works
 
       self.Size = Size(450, 400)                                  # dimension of the Form
       self.CenterToScreen()                                       # Form is being centered to screen
  
 
   def OnSelected(self, sender, event):                                    # On selected function fo event
        #print sender.Items[event.Index].SubItems[0].Text
        #senderlist.append(sender.Items[event.Index].SubItems[0].Text)     
        if event.CurrentValue.ToString() == "Unchecked":                    # if item is unchecked, when I check it add parameter to senderlist
            senderlist.append(sender.Items[event.Index].SubItems[0].Text)  
        if event.CurrentValue.ToString() == "Checked":                      # if item is checked, when I uncheck it remove parameter from senderlist
            senderlist.remove(sender.Items[event.Index].SubItems[0].Text)
        #   print event.CurrentValue.ToString()
 
   def OnColumnClick(self, sender, event):                                 # this is used only to sort listview items whe column is being clicked. Works only on main item, not on subitems
       if sender.Sorting == SortOrder.Ascending:
           sender.Sorting = SortOrder.Descending
       else:
           sender.Sorting = SortOrder.Ascending
  
  
   def OnClick(self,sender,event):                                        # when button "Delete Parameters" is being clicked
       t = Transaction(doc, 'Delete multiple parameters')                 # this creates Revit transaction which enables changes in document
       t.Start()                                                          # Transaction starts
       for i in editableParams:                                           # for non Built-in parameters
          if (i.Definition.Name.ToString() in senderlist):                # if parameter is being selected (ticked)
           mgr.RemoveParameter(i)                                         # remove parameter
           # TaskDialog.Show("dd","ro")                                   # I used this only as a test to count how many parameters have been deleted
       if len(senderlist)>0:                                              # if any parameter is selected
           TaskDialog.Show("Parameters deleted"," All selected non Built-in parameters have been deleted")
       else:                                                              # if none is selected
           TaskDialog.Show("None selected","Parameters were not selected")
       t.Commit()                                                         # This closes transaction
       self.Close()                                                       # This closes window form
      
Application.Run(IForm())                                                    #Windows form initiated