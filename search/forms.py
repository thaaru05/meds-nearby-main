from django import forms 
medicines=[('','search'),
           ('Lobate Cream', 'Lobate Cream'), 
           ('Liv 52 DS Tablet', 'Liv 52 DS Tablet'), 
           ('Morr F 5% Solution', 'Morr F 5% Solution'), 
           ('Omez FF 40mg Tablet', 'Omez FF 40mg Tablet'), 
           ('Parit 20mg Tablet', 'Parit 20mg Tablet'), 
           ('Progynova 1mg Tablet', 'Progynova 1mg Tablet'), 
           ('Prosure Powder', 'Prosure Powder'), 
           ('Urispas 200mg Tablet', 'Urispas 200mg Tablet'), 
           ('Qilib Men Lotion', 'Qilib Men Lotion'), 
           ('Paragis D 20mg/650mg Tablet', 'Paragis D 20mg/650mg Tablet'), 
           ('Quadriderm NF Cream', 'Quadriderm NF Cream'), 
           ('Seretide Evohaler 50mcg/100mcg Inhaler', 'Seretide Evohaler 50mcg/100mcg Inhaler'), 
           ('Sirdalud 2mg Tablet', 'Sirdalud 2mg Tablet'), 
           ('Stablon 12.5mg Tablet', 'Stablon 12.5mg Tablet'), 
           ('Stugeron 25mg Tablet', 'Stugeron 25mg Tablet'), 
           ('Swich O Tablet', 'Swich O Tablet'), 
           ('Synaptol 100mg Tablet', 'Synaptol 100mg Tablet'), 
           ('Telma ACT Tablet 40mg/5mg/12.5mg', 'Telma ACT Tablet 40mg/5mg/12.5mg'), 
           ('Tfil 10mg Tablet', 'Tfil 10mg Tablet'), 
           ('Trajenta 5mg Tablet', 'Trajenta 5mg Tablet')]
sort_=[('d','distance'),('p','price')]
class SearchForm(forms.Form):
    medicine=forms.ChoiceField(choices=medicines)
    postal_code=forms.CharField()
    search_radius_in_meter=forms.CharField(initial='4000')
    sortby=forms.ChoiceField(choices=sort_)

class CoordForm(forms.Form):
    to_lat=forms.CharField(widget=forms.HiddenInput)
    to_lon=forms.CharField(widget=forms.HiddenInput)
    frm_lat=forms.CharField(widget=forms.HiddenInput)
    frm_lon=forms.CharField(widget=forms.HiddenInput)
