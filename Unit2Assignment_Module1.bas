Attribute VB_Name = "Module1"
Sub volume()

Dim LastRow As Long
LastRow = Cells(Rows.Count, 1).End(xlUp).Row

Cells(1, 10) = "ticker"
Cells(1, 11) = "Total stock volume"

Dim ticker As String
Dim volume As Double

volume = 0

Dim summarytable_row As Integer
summarytable_row = 2

For i = 2 To LastRow
If Cells(i + 1, 1).Value <> Cells(i, 1) Then
ticker = Cells(i, 1).Value
volume = volume + Cells(i, 7)
Range("J" & summarytable_row).Value = ticker
Range("K" & summarytable_row).Value = volume
summarytable_row = summarytable_row + 1
volume = 0

Else
volume = volume + Cells(i, 7).Value


End If

Next i

End Sub
Sub eachws()

Dim xSh As Worksheet
   Application.ScreenUpdating = False
   For Each xSh In Worksheets
       xSh.Select
       Call volume
   Next
   Application.ScreenUpdating = True
   
End Sub
