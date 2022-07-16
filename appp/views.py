from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Service
from django.contrib.auth.models import User,auth
from django.contrib.auth import login
from products.models import Product,StockTrack
from clients.models import Client
from orders.models import SupplierOrder,ClientOrder
from suppliers.models import Supplier

#
from django.contrib import messages
from django.utils import timezone
from django.forms import inlineformset_factory
import csv
from xlsxwriter.workbook import Workbook
import io
from utils import render_to_pdf,maxx

#
from neworders.forms import nOrderCForm,nClientOrderForm,nSupplierOrderForm
from neworders.models import nOrderS,nOrderC,nSupplierOrder,nClientOrder


def init_stock_track(request):
    today = timezone.now().date()
    stocktraking = request.user.stocktracklist.order_by('Date')
    if stocktraking.count() == 0 : 
        newTrack = StockTrack(
            Stock = 0,
            In = 0,
            Out = 0,
            Date = today
        )
        newTrack.save()
        request.user.stocktracklist.add(newTrack)
def product_stock_track(product,request):
    today=timezone.now().date()
    stocktraking = request.user.stocktracklist.order_by('Date')
    if stocktraking.count() > 0:
        b= False
        for t in stocktraking:
            if t.Date == today:
                b=True
                st=t
        if b:
            st.Stock = int(st.Stock) + int(product.Quantity)
            st.In = int(st.In) + int(product.Quantity)
            st.save()
        else:
            newTrack = StockTrack(
                Stock = int(stocktraking.reverse()[0].Stock) + int(product.Quantity),
                In = int(product.Quantity),
                Date = today
            )

            newTrack.save()
            request.user.stocktracklist.add(newTrack)
    if stocktraking.count() == 0:
        if int(product.Quantity) > -1 :
            newTrack = StockTrack(
                    
                    Stock = int(product.Quantity),
                    In = int(product.Quantity),
                    Out = 0,
                    Date = today
                )
        if int (product.Quantity) < 0 :
            newTrack = StockTrack(
                    
                    Stock = 0,
                    In = 0,
                    Out = 0,
                    Date = today
                )
        newTrack.save()
        request.user.stocktracklist.add(newTrack)

def delete_product_stock_track(product,request):
    today=timezone.now().date()
    stocktraking = request.user.stocktracklist.order_by('Date')
    if stocktraking.count() > 0:
        b= False
        for t in stocktraking:
            if t.Date == today:
                b=True
                st=t
        if b:
            st.Stock = int(st.Stock) - int(product.Quantity)
            st.Out = int(product.Quantity)
            st.save()
        else:
            newTrack = StockTrack(
                Stock = int(stocktraking.reverse()[0].Stock) - int(product.Quantity),
                Out = int(product.Quantity),
                In = 0,
                Date = today
            )

            newTrack.save()
            request.user.stocktracklist.add(newTrack)
    

def create_stock_track_client_confirm(request,order):
    stocktraking = request.user.stocktracklist.order_by('Date')
    b = False
    for t in stocktraking:
        if order.Date == t.Date :
            b = True
            st = t
    if b : 
        st.Stock = st.Stock - int(stockoforderC(order))
        st.Out = int(stockoforderC(order))
        st.save()
    else:
        newTrack = StockTrack(
            Stock = stocktraking.reverse()[0].Stock - stockoforderC(order),
            Out = stockoforderC(order),
            In = 0,
            Date = order.Date
        )
        newTrack.save()
        request.user.stocktracklist.add(newTrack)

def QoforderC(order):
    listorder = order.norderclist.all()
    t=0
    for o in listorder:
        t = t + o.Quantity   
    return t

def QoforderS(order):
    listorder = order.norderslist.all()
    t=0
    for o in listorder:
        t = t + o.Quantity   
    return t

def stockoforderC(order):
    listorder = order.norderclist.all()
    t=0
    for o in listorder:
        t = t + o.Product.Quantity   
    return t
     

def create_stock_track_client(request,order):  #xz

    stocktraking = request.user.stocktracklist.order_by('Date')
    b = False
    for t in stocktraking:
        if order.Date == t.Date :
            b = True
            st = t
    if b : 
        st.Stock = st.Stock - QoforderC(order)
        st.Out = QoforderC(order)
        st.save()
    else:
        if order.Date <  stocktraking.reverse()[0].Date :
            newTrack = StockTrack(
                Stock = 0,
                In = 0,
                Out = 0,
                Date = order.Date
            )
            newTrack.save()
            Newstocktraking = request.user.stocktracklist.order_by('Date')
            ii=0
            sti = 0
            print("we here 1 --------------------------")
            for tt in Newstocktraking:
                if order.Date == tt.Date :
                    b = True
                    st = t
                    sti = ii +1
                else : ii = ii + 1

            newTrack.Stock = Newstocktraking[sti].Stock  - QoforderC(order) 
            newTrack.Out = QoforderC(order) 
            newTrack.save()
            print("we here 2 --------------------------")

        else :
            newTrack = StockTrack(
                Stock = stocktraking.reverse()[0].Stock - QoforderC(order),
                Out = QoforderC(order),
                In = 0,
                Date = order.Date
            )
            newTrack.save()

        
        request.user.stocktracklist.add(newTrack)

def create_stock_track_supplier(request,order):
    stocktraking = request.user.stocktracklist.order_by('Date')
    b = False
    for t in stocktraking:
        if order.Date == t.Date :
            b = True
            st = t
    if b : 
        st.Stock = st.Stock + QoforderS(order)
        st.In = st.In + QoforderS(order)
        st.save()
    else:
        if order.Date <  stocktraking.reverse()[0].Date :
            newTrack = StockTrack(
                Stock = QoforderS(order),
                In = QoforderS(order),
                Out = 0,
                Date = order.Date
            )
        else:    
            
            newTrack = StockTrack(
                Stock = stocktraking.reverse()[0].Stock + QoforderS(order),
                In = QoforderS(order),
                Out = 0,
                Date = order.Date
            )
            newTrack.save()
            request.user.stocktracklist.add(newTrack)
        


def info(request):
    Ocount= request.user.nclientorderlist.all().count()+request.user.nsupplierorderlist.all().count()
    list_products= request.user.productlist.all()
    OScount= request.user.nsupplierorderlist.all().count()
    OCcount= request.user.nclientorderlist.all().count()

    OSPcount=list_order_suppliers= request.user.nsupplierorderlist.filter(Status='en attente').count()
    OCPcount=list_order_clients= request.user.nclientorderlist.filter(Status='en attente').count()
    
    strack=[]
    dtrack=[]
    intrack=[]
    outtrack=[]
    stocktraking = request.user.stocktracklist.order_by('Date')[:30]
    for t in stocktraking:
        strack.append(int(t.Stock))
        intrack.append(int(t.In))
        outtrack.append(int(t.Out))
        dtrack.append(str(t.Date))
    

    PendingOrdersCount=OCPcount + OSPcount
    repture_count=0
    stock_neg=0
    nbstock_neg=0
    notif=False
    for entry in list_products:
        if entry.Quantity == 0:
            repture_count=repture_count+ 1
        if entry.Quantity<0 :
            stock_neg=stock_neg+1
            nbstock_neg=nbstock_neg+entry.Quantity
    if ((repture_count > 0) or (nbstock_neg < 0)):
        notif=True
    
    context= {
        "stock_neg": stock_neg,
        "notif": notif,
        "outtrack": outtrack,
        "intrack": intrack,
        "OScount": OScount,
        "OCcount": OCcount,
        "PendingOrdersCount": PendingOrdersCount,
        "repture_count": repture_count,
        "Ocount": Ocount,
        "today": timezone.now().date(),
        "dtrack": dtrack,
        "strack": strack,
        "nbstock_neg": int(nbstock_neg)
    }
    return(context)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else: 
        return render(request,"index.html",{})

def dashboard(request):

    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()

    
    list_products= request.user.productlist.all()
    repture_count=0
    stock_count=0
    stock_neg=0
    nbstock_neg=0
    notif=False
    for entry in list_products:
        if entry.Quantity>0:
            stock_count=stock_count+ entry.Quantity
        if entry.Quantity == 0:
            repture_count=repture_count+ 1
        if entry.Quantity<0 :
            stock_neg=stock_neg+1
            nbstock_neg=nbstock_neg+entry.Quantity
    if ((repture_count > 0) or (nbstock_neg < 0)):
        notif=True
    context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "stock_count": int(stock_count),
        "stock_neg": stock_neg,
        "notif": notif,
        "repture_count": repture_count,
        "nbstock_neg": int(nbstock_neg)
    }
    context.update(info(request))
    return render(request,"dashboard/dashboard.html",context)

def account(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password1 == password2):
            if(request.user.username != username):
                if(User.objects.filter(username=username).exists()):
                    
                    messages.info(request,'nom d utilisateur exist deja')
                else:    
                    if not password1:
                        request.user.username=username 
                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        pwd= request.user.password
                         
                        request.user.save()
                        user = auth.authenticate(username=username,password=pwd)
                        login(request,user)                        
                        
                        return redirect('account')
                        
                    else:
                        request.user.set_password(password1)
                        request.user.username=username 
                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        request.user.save()
                        user = auth.authenticate(username=username,password=password1)
                        login(request,user) 
                        return redirect('account')
                        
            else :  
                    
                    if not password1:

                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        pwd= request.user.password
                        usr= request.user.username
                        request.user.save()
                        user = auth.authenticate(username=usr,password=pwd)
                        login(request,user) 
                        return redirect('account')
                    else:
                        request.user.set_password(password1) 
                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        usr= request.user.username
                        request.user.save()
                        user = auth.authenticate(username=usr,password=password1)
                        login(request,user) 
                        return redirect('account')
              
        else:
            messages.info(request,'les mots de passe ne correspondent pas')

        return redirect('account')
    else:
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
        }
        context.update(info(request))
        return render(request,"dashboard/account.html",context)
    

def product_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        purchaseprice = request.POST['purchaseprice']
        salesprice = request.POST['salesprice']
        reference = request.POST['reference']
        manufacturer = request.POST['manufacturer']
        suppliers = request.POST.getlist('suppliers')
        category = request.POST['category']
        quantity = request.POST['quantity']
        error= False
        if not title : 
            messages.info(request,'Le champ titre ne peut pas etre vide')
            error=True
        if not purchaseprice : 
            messages.info(request,'Le champ Prix dachat ne peut pas etre vide')
            error=True
        if not salesprice : 
            messages.info(request,'Le champ Prix de vente ne peut pas etre vide')
            error=True
        if not reference : 
            messages.info(request,'Le champ reference ne peut pas etre vide')
            error=True
        if not manufacturer : 
            messages.info(request,'Le champ Fabricant ne peut pas etre vide')
            error=True
        if not category : 
            messages.info(request,'Le champ Categorie ne peut pas etre vide')
            error=True
        if not quantity : 
            messages.info(request,'Le champ quantité ne peut pas etre vide')
            error=True
        if not suppliers : 
            messages.info(request,'Le champ Fournisseurs  ne peut pas etre vide')
            error=True
        if error:
            return redirect('product_create')


        product = Product(
            Title=title, 
            Description=description,
            PurchasePrice=purchaseprice,
            SalesPrice = salesprice,
            Reference = reference,
            Manufacturer = manufacturer,
            #Suppliers = suppliers,
            Category = category,
            Quantity = quantity
        )
        product.save()
        for s in suppliers:
            Sobj=Supplier.objects.get(Name=s)
            Sobj.save()
            product.Suppliers.add(Sobj)
        #product.Suppliers.set(suppliers)
        request.user.productlist.add(product)
        product_stock_track(product,request)
        init_stock_track(request)
        messages.info(request,'Produit Ajouté')
        return redirect('product_list')

    else:
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()

        list_suppliers= request.user.supplierlist.all()
        
        
        context = {
            "list_suppliers" : list_suppliers,
            "Pcount": Pcount,
            "Ccount": Ccount,
            "Scount": Scount
        }
        context.update(info(request))
        return render(request,"dashboard/product/product_create.html",context)

def product_edit(request, id):
    obj = get_object_or_404(Product, id=id)
    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()    
    list_suppliers= request.user.supplierlist.all()
    list_suppliers_obj=[]
    for s in obj.Suppliers.all():
        list_suppliers_obj.append(s.Name)

    
    context = {
        "list_suppliers" : list_suppliers,
        "list_suppliers_obj" : list_suppliers_obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        
        "obj":obj
    }
    context.update(info(request))

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        purchaseprice = request.POST['purchaseprice']
        salesprice = request.POST['salesprice']
        reference = request.POST['reference']
        manufacturer = request.POST['manufacturer']
        suppliers = request.POST.getlist('suppliers')
        category = request.POST['category']
        quantity = request.POST['quantity']

        error= False
        if not title : 
            messages.info(request,'Le champ titre ne peut pas etre vide')
            error=True
        if not purchaseprice : 
            messages.info(request,'Le champ Prix dachat ne peut pas etre vide')
            error=True
        if not salesprice : 
            messages.info(request,'Le champ Prix de vente ne peut pas etre vide')
            error=True
        if not reference : 
            messages.info(request,'Le champ reference ne peut pas etre vide')
            error=True
        if not manufacturer : 
            messages.info(request,'Le champ Fabricant ne peut pas etre vide')
            error=True
        if not category : 
            messages.info(request,'Le champ Categorie ne peut pas etre vide')
            error=True
        if not quantity : 
            messages.info(request,'Le champ quantité ne peut pas etre vide')
            error=True
        if not suppliers : 
            messages.info(request,'Le champ Fournisseurs  ne peut pas etre vide')
            error=True
        if error:
            context.update(info(request))
            return render(request,"dashboard/product/product_edit.html",context)

        obj.Title = title
        obj.Description = description
        obj.PurchasePrice = purchaseprice
        obj.SalesPrice = salesprice
        obj.Reference = reference
        obj.Manufacturer = manufacturer
        #obj.Suppliers = suppliers
        obj.Category = category
        obj.Quantity = quantity
        for s in suppliers:
            Sobj=request.user.supplierlist.get(Name=s)
            #Sobj=Supplier.objects.get(Name=s)
            Sobj.save()
            obj.Suppliers.add(Sobj)


        obj.save()
        messages.info(request,'Produit Sauvgardé')
        return redirect('product_list')

    else:
        context.update(info(request))
        return render(request,"dashboard/product/product_edit.html",context)

def product_list(request):
    list_products= request.user.productlist.all() 
    if request.method == 'POST':
        if 'del' in request.POST:
            selectedlist = request.POST.getlist('selectedlist')
            for i in selectedlist:
                #obj=get_object_or_404(Product, id=int(i))
                obj = Product.objects.get(id=int(i))
                delete_product_stock_track(obj,request)
                obj.delete() 
            return redirect('product_list') 
        if 'xls' in request.POST: 

            output = io.BytesIO()

            workbook = Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()

            worksheet.write(4, 0, "Titre")
            worksheet.write(4, 1, "Prix d'achat")
            worksheet.write(4, 2, "Prix de vente")
            worksheet.write(4, 3, "Reference")
            worksheet.write(4, 4, "Fabricant")
            worksheet.write(4, 5, "Fournisseurs")
            worksheet.write(4, 6, "Categorie")
            worksheet.write(4, 7, "Quantité")

            i=5
            for entry in list_products:
                #writer.writerow([o.Product,o.Product.SalesPrice,o.Quantity,o.line_total() ])
                worksheet.write(i, 0, entry.Title)
                worksheet.write(i, 1, entry.PurchasePrice)
                worksheet.write(i, 2, entry.SalesPrice)
                worksheet.write(i, 3, entry.Reference)
                worksheet.write(i, 4, entry.Manufacturer)
                s=""
                for ss in entry.Suppliers.all():
                    s = s + ss.Name +","
                worksheet.write(i, 5, s)
                worksheet.write(i, 6, entry.Category)
                worksheet.write(i, 7, entry.Quantity)
                i=i+1

            workbook.close()

            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")            
            filen = "produits.xlsx"
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filen)

            output.close()
            return response
        if 'pdf' in request.POST: 
            context = {
                "list_products" : list_products
            }

            return render_to_pdf("other/product_list.html",context)
     

    else:
           
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()


        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_products" : list_products
        }
        context.update(info(request))
        return render(request,"dashboard/product/product_list.html",context)


def product_delete(request, id):
    obj=get_object_or_404(Product, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('product_list')
    else:    
        
        list_products= request.user.productlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count() 
        context= {
            "obj":obj,
            "Pcount": Pcount,
            "Ccount": Ccount,
            "Scount": Scount,
            "list_products" : list_products
        }
        context.update(info(request))
        return render(request,"dashboard/product/product_delete.html",context)


def reptureproduct_list(request):
    
    
    list_products= request.user.productlist.all()
   
    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()

    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "list_products" : list_products
    }
    context.update(info(request))
    return render(request,"dashboard/product/reptureroduct_list.html",context)
def negproduct_list(request):
    
    
    list_products= request.user.productlist.all()
    
    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()


    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "list_products" : list_products
    }
    context.update(info(request))
    return render(request,"dashboard/product/negproduct_list.html",context)

def client_create(request):
    if request.method == 'POST':
        Type = request.POST['type']
        Name = request.POST['name']
        Phone = request.POST['phone']
        Email = request.POST['email']
        Reference = request.POST['reference']
        Adress = request.POST['adress']
        Note = request.POST['note']
        
        error= False
        if not Name : 
            messages.info(request,'Le champ Nom  ne peut pas etre vide')
            error=True
        if not Phone : 
            messages.info(request,'Le champ Numero telephone  ne peut pas etre vide')
            error=True
        if not Reference : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if not Adress : 
            messages.info(request,'Le champ addresse ne peut pas etre vide')
            error=True
        if error:
            return redirect('client_create')

        client = Client(
            Type = Type,
            Name = Name,
            Phone = Phone,
            Email = Email,
            Reference = Reference,
            Adress = Adress,
            Note = Note
        )
        client.save()
        messages.info(request,'Client Ajouté')
        request.user.clientlist.add(client)
        return redirect('client_list')

    else:
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
    }
        context.update(info(request))
        return render(request,"dashboard/client/client_create.html",context)

def client_edit(request,id):
    obj = get_object_or_404(Client, id=id)
    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()
    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "obj":obj
    }
    
    if request.method == 'POST':
        Type = request.POST['type']
        Name = request.POST['name']
        Phone = request.POST['phone']
        Email = request.POST['email']
        Reference = request.POST['reference']
        Adress = request.POST['adress']
        Note = request.POST['note']
        
        error= False
        if not Name : 
            messages.info(request,'Le champ Nom  ne peut pas etre vide')
            error=True
        if not Phone : 
            messages.info(request,'Le champ Numero telephone  ne peut pas etre vide')
            error=True
        if not Reference : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if not Adress : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if error:
            context.update(info(request))
            return render(request,"dashboard/client/client_edit.html",context)

        
        obj.Type = Type
        obj.Name = Name
        obj.Phone = Phone
        obj.Email = Email
        obj.Reference = Reference
        obj.Adress = Adress
        obj.Note = Note
        
        obj.save()
        messages.info(request,'Client modifié')
        return redirect('client_list')

    else:
        context.update(info(request))
        return render(request,"dashboard/client/client_edit.html",context)

def client_list(request): #zz
    list_clients= request.user.clientlist.all()
    if request.method == 'POST':
        if 'del' in request.POST:
            selectedlist = request.POST.getlist('selectedlist')
            for i in selectedlist:
                obj = Client.objects.get(id=int(i))
                obj.delete() 
            return redirect('client_list')    
        if 'xls' in request.POST: 

            output = io.BytesIO()

            workbook = Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()

            worksheet.write(4, 0, "Type")
            worksheet.write(4, 1, "Nom")
            worksheet.write(4, 2, "Telephone")
            worksheet.write(4, 3, "Email")
            worksheet.write(4, 4, "Référence")
            worksheet.write(4, 5, "Adresse")
            worksheet.write(4, 6, "Note")
            
            mx = 2

            i=5
            for entry in list_clients:
                #writer.writerow([o.Product,o.Product.SalesPrice,o.Quantity,o.line_total() ])
                worksheet.write(i, 0, entry.Type)
                mx = maxx(mx , len(entry.Type) )
                worksheet.write(i, 1, entry.Name)
                mx = maxx(mx , len(entry.Name) )
                worksheet.write(i, 2, str(entry.Phone))
                mx = maxx(mx , len(entry.Phone) )
                worksheet.write(i, 3, entry.Email)
                mx = maxx(mx , len(entry.Email) )
                worksheet.write(i, 4, entry.Reference)
                mx = maxx(mx , len(entry.Reference) )
                worksheet.write(i, 5, entry.Adress)
                mx = maxx(mx , len(entry.Adress) )
                worksheet.write(i, 6, entry.Note)
                mx = maxx(mx , len(entry.Note) )
                
                i=i+1

            for k in range(0,6):
                worksheet.set_column(0, k, mx)
            print(" mx ===============",mx)
            workbook.close()

            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")            
            filen = "produits.xlsx"
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filen)

            output.close()
            return response
        if 'pdf' in request.POST: 
            context = {
                "list_clients" : list_clients 
            }

            return render_to_pdf("other/client_list.html",context)

          

    else:

        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_clients" : list_clients
        }
        context.update(info(request))
        return render(request,"dashboard/client/client_list.html",context)


def client_delete(request, id):
    obj=get_object_or_404(Client, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('client_list')
    else:
       
        list_clients= request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "obj":obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_clients" : list_clients
        }
        context.update(info(request))
        return render(request,"dashboard/client/client_delete.html",context)

def supplier_create(request):
    if request.method == 'POST':
        Type = request.POST['type']
        Name = request.POST['name']
        Phone = request.POST['phone']
        Category = request.POST['category']
        Reference = request.POST['reference']
        Adress = request.POST['adress']
        Note = request.POST['note']
        
        error= False
        if not Name : 
            messages.info(request,'Le champ Nom  ne peut pas etre vide')
            error=True
        if not Phone : 
            messages.info(request,'Le champ Numero telephone  ne peut pas etre vide')
            error=True
        if not Reference : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if not Adress : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if not Category : 
            messages.info(request,'Le champ Categorie ne peut pas etre vide')
            error=True

        if error:
            return redirect('supplier_create')

        supplier = Supplier(
            Type = Type,
            Name = Name,
            Phone = Phone,
            Category = Category,
            Reference = Reference,
            Adress = Adress,
            Note = Note
        )
        supplier.save()
        request.user.supplierlist.add(supplier)  
        messages.info(request,'Fournisseur Ajouté')
        return redirect('supplier_list')

    else:
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
    }
        context.update(info(request))
        return render(request,"dashboard/supplier/supplier_create.html",context)

def supplier_createPOPUP(request):
    if request.method == 'POST':
        Type = request.POST['type']
        Name = request.POST['name']
        Phone = request.POST['phone']
        Category = request.POST['category']
        Reference = request.POST['reference']
        Adress = request.POST['adress']
        Note = request.POST['note']
        
        error= False
        if not Name : 
            messages.info(request,'Le champ Nom  ne peut pas etre vide')
            error=True
        if not Phone : 
            messages.info(request,'Le champ Numero telephone  ne peut pas etre vide')
            error=True
        if not Reference : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if not Adress : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if not Category : 
            messages.info(request,'Le champ Categorie ne peut pas etre vide')
            error=True

        if error:
            return redirect('supplier_createPOPUP')

        supplier = Supplier(
            Type = Type,
            Name = Name,
            Phone = Phone,
            Category = Category,
            Reference = Reference,
            Adress = Adress,
            Note = Note
        )
        supplier.save()
        request.user.supplierlist.add(supplier)  
        messages.info(request,'Fournisseur Ajouté')
        return redirect('supplier_close')

    else:
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
    }
        context.update(info(request))
        return render(request,"dashboard/supplier/supplier_create.html",context)

def supplier_close(request):
    return render(request,"dashboard/supplier/supplier_close.html",{})

def supplier_edit(request,id=id):
    obj = get_object_or_404(Supplier, id=id)
    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()
    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "obj":obj
    }
    
    if request.method == 'POST':
        Type = request.POST['type']
        Name = request.POST['name']
        Phone = request.POST['phone']
        Category = request.POST['category']
        Reference = request.POST['reference']
        Adress = request.POST['adress']
        Note = request.POST['note']
        
        error= False
        if not Name : 
            messages.info(request,'Le champ Nom  ne peut pas etre vide')
            error=True
        if not Phone : 
            messages.info(request,'Le champ Numero telephone  ne peut pas etre vide')
            error=True
        if not Reference : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if not Adress : 
            messages.info(request,'Le champ Adress ne peut pas etre vide')
            error=True
        if not Category : 
            messages.info(request,'Le champ Categorie ne peut pas etre vide')
            error=True

        if error:
            context.update(info(request))
            return render(request,"dashboard/supplier/supplier_edit.html",context)


        obj.Type = Type
        obj.Name = Name
        obj.Phone = Phone
        obj.Category = Category
        obj.Reference = Reference
        obj.Adress = Adress
        obj.Note = Note

        obj.save()
        messages.info(request,'Fournisseur Modifié')
        return redirect('supplier_list')

    else:
        context.update(info(request))
        return render(request,"dashboard/supplier/supplier_edit.html",context)

def supplier_list(request):
    list_suppliers= request.user.supplierlist.all()
    if request.method == 'POST':
        if 'del' in request.POST:
            selectedlist = request.POST.getlist('selectedlist')
            for i in selectedlist:
                #obj=get_object_or_404(Product, id=int(i))
                obj = Supplier.objects.get(id=int(i))
                obj.delete() 
            return redirect('supplier_list') 
        if 'xls' in request.POST: 

            output = io.BytesIO()

            workbook = Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()

            worksheet.write(4, 0, "Type")
            worksheet.write(4, 1, "Nom")
            worksheet.write(4, 2, "Telephone")
            worksheet.write(4, 3, "Email")
            worksheet.write(4, 4, "Référence")
            worksheet.write(4, 5, "Adresse")
            worksheet.write(4, 6, "Note")
            
            mx = 2

            i=5
            for entry in list_suppliers:
                #writer.writerow([o.Product,o.Product.SalesPrice,o.Quantity,o.line_total() ])
                worksheet.write(i, 0, entry.Type)
                mx = maxx(mx , len(entry.Type) )
                worksheet.write(i, 1, entry.Name)
                mx = maxx(mx , len(entry.Name) )
                worksheet.write(i, 2, str(entry.Phone))
                mx = maxx(mx , len(entry.Phone) )

                worksheet.write(i, 3, entry.Reference)
                mx = maxx(mx , len(entry.Reference) )
                worksheet.write(i, 4, entry.Category)
                mx = maxx(mx , len(entry.Category) )
                worksheet.write(i, 5, entry.Adress)
                mx = maxx(mx , len(entry.Adress) )
                worksheet.write(i, 6, entry.Note)
                mx = maxx(mx , len(entry.Note) )
                
                i=i+1

            for k in range(0,6):
                worksheet.set_column(0, k, mx)
            print(" mx ===============",mx)
            workbook.close()

            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")            
            filen = "produits.xlsx"
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filen)

            output.close()
            return response
        if 'pdf' in request.POST: 
            context = {
                "list_suppliers" : list_suppliers 
            }

            return render_to_pdf("other/supplier_list.html",context)     
    else:
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()

        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_suppliers" : list_suppliers
        }
        context.update(info(request))
        return render(request,"dashboard/supplier/supplier_list.html",context)
def supplier_delete(request,id=id):
    obj=get_object_or_404(Supplier, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('supplier_list')    

    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()
    suppliers = Supplier.objects.all()
    list_suppliers= request.user.supplierlist.all()
    context= {
    "obj":obj,
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "list_suppliers" : list_suppliers
    }

    context.update(info(request))
    return render(request,"dashboard/supplier/supplier_delete.html",context)



def PendingOrders_list(request):
    if request.method == 'POST':
        selectedlist = request.POST.getlist('selectedlist')
    
    else:
        list_order_suppliers= request.user.nsupplierorderlist.filter(Status='en attente')
        list_order_clients= request.user.nclientorderlist.filter(Status='en attente')

        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_order_clients" : list_order_clients,
        "list_order_suppliers" : list_order_suppliers
        }
        context.update(info(request))
        return render(request,"dashboard/order/pendingOrders_list.html",context)
        
def order_client_list(request):
    if request.method == 'POST':
        selectedlist = request.POST.getlist('selectedlist')

        for i in selectedlist:
            #obj = ClientOrder.objects.get(id=int(i))
            obj = nClientOrder.objects.get(id=int(i))
            obj.delete() 
        return redirect('order_client_list')      

    else:
        #list_order_clients= request.user.clientorderlist.all()
        list_order_clients= request.user.nclientorderlist.all()
        lsclient=[]
        for o in list_order_clients:
            if o.Client not in lsclient:  #zebi
                lsclient.append(o.Client)
         
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        clientt = request.GET.get('client')
        status = request.GET.get('status')
        date_de = request.GET.get('de')
        date_vers = request.GET.get('vers')
        if clientt is not None and clientt != "-------":
            list_order_clients = list_order_clients.filter(Client=clientt)
        if status is not None and status != "-------":
            list_order_clients = list_order_clients.filter(Status=status)
        if date_de is not None:
            if date_vers is not None:
                list_order_clients = list_order_clients.filter(Date__gte=date_de,Date__lte=date_vers)
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "lsclient": lsclient,
        "list_order_clients" : list_order_clients
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_list.html",context)

def order_pending_list(request):
    if request.method == 'POST':
        selectedlist = request.POST.getlist('selectedlist')

        for i in selectedlist:
            obj = ClientOrder.objects.get(id=int(i))
            obj.delete() 
        return redirect('order_client_list')      

    else:
        list_order_clients= request.user.clientorderlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_order_clients" : list_order_clients
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_list.html",context)

def order_supplier_list(request):
    # if request.method == 'POST':
    #     selectedlist = request.POST.getlist('selectedlist')

    #     for i in selectedlist:
    #         obj = SupplierOrder.objects.get(id=int(i))
    #         obj.delete() 
    #     return redirect('order_supplier_list')      

    # else:
    #     list_order_suppliers= request.user.supplierorderlist.all()
    #     Pcount= request.user.productlist.all().count()
    #     Ccount= request.user.clientlist.all().count()
    #     Scount= request.user.supplierlist.all().count()
    #     context= {
    #     "Pcount": Pcount,
    #     "Ccount": Ccount,
    #     "Scount": Scount,
    #     "list_order_suppliers" : list_order_suppliers
    #     }
    #     context.update(info(request))
    #     return render(request,"dashboard/order/order_supplier_list.html",context)
    if request.method == 'POST':
        selectedlist = request.POST.getlist('selectedlist')

        for i in selectedlist:
            #obj = ClientOrder.objects.get(id=int(i))
            obj = nSupplierOrder.objects.get(id=int(i))
            obj.delete() 
        return redirect('order_supplier_list')      

    else:
        
        #list_order_clients= request.user.clientorderlist.all()
        list_order_supplier= request.user.nsupplierorderlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        lssupplier=[]
        for o in list_order_supplier:
            if o.Supplier not in lssupplier:  #zebi
                lssupplier.append(o.Supplier)

        status = request.GET.get('status')
        supplier = request.GET.get('supplier')
        date_de = request.GET.get('de')
        date_vers = request.GET.get('vers')
        if status is not None and status != "-------":
            list_order_supplier = list_order_supplier.filter(Status=status)
        if supplier is not None and supplier != "-------":
            list_order_supplier = list_order_supplier.filter(Supplier=supplier)
        if date_de is not None:
            if date_vers is not None:
                list_order_supplier = list_order_supplier.filter(Date__gte=date_de,Date__lte=date_vers)

        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "lssupplier": lssupplier,
        "list_order_supplier" : list_order_supplier
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_supplier_list.html",context)

def nClientOrder_create(request):
    if request.method == 'POST':
        
        P = request.POST['product']
        Pobj = Product.objects.get(id=P)
        Pobj.save() 
        C = request.POST['client']
        Cobj = Client.objects.get(id=C)
        Cobj.save()


        Quantity = request.POST['quantity']
        Total = float(Quantity) * float(Pobj.SalesPrice)
        Date = request.POST['date']
        Status =  "en attente"
        error= False
        if not Product : 
            messages.info(request,'Le champ Product ne peut pas etre vide')
            error=True
        if not Client : 
            messages.info(request,'Le champ Client  ne peut pas etre vide')
            error=True
        if not Quantity : 
            messages.info(request,'Le champ Quantity ne peut pas etre vide')
            error=True
        if not Date : 
            messages.info(request,'Le champ Date ne peut pas etre vide')
            error=True
        if not Status : 
            messages.info(request,'Le champ Status ne peut pas etre vide')
            error=True
        if error:
            return redirect('order_client_create')
        
        cOrder = ClientOrder(
            Quantity = Quantity,
            Date = Date,
            Status = Status,
            Total = Total
        )
        cOrder.save()
        
        request.user.clientorderlist.add(cOrder)
        Pobj.clientorderlist.add(cOrder)
        Cobj.clientorderlist.add(cOrder)

        messages.info(request,'Commande Ajouté')
        
        return redirect('order_client_list')

    else:
        productlist=request.user.productlist.all()
        clientlist=request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "productlist": productlist,
        "clientlist": clientlist,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
    }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_create.html",context)

def order_supplier_create(request):
    # if request.method == 'POST':        
    #     P = request.POST['product']
    #     Pobj = Product.objects.get(id=P)
    #     Pobj.save() 
    #     S = request.POST['supplier']
    #     Sobj = Supplier.objects.get(id=S)
    #     Sobj.save()
    #     Quantity = request.POST['quantity']
    #     Date = request.POST['date']
    #     Status = "en attente"
    #     Total = float(Quantity) * float(Pobj.PurchasePrice)
    #     error= False
    #     if not Product : 
    #         messages.info(request,'Le champ Product ne peut pas etre vide')
    #         error=True
    #     if not Client : 
    #         messages.info(request,'Le champ Supplier  ne peut pas etre vide')
    #         error=True
    #     if not Quantity : 
    #         messages.info(request,'Le champ Quantity ne peut pas etre vide')
    #         error=True
    #     if not Date : 
    #         messages.info(request,'Le champ Date ne peut pas etre vide')
    #         error=True
        
    #     if error:
    #         return redirect('order_supplier_create')
       
    #     sOrder = SupplierOrder(
    #         Quantity = Quantity,
    #         Date = Date,
    #         Total = Total,
    #         Status = Status
    #     )
    #     sOrder.save()
        
    #     request.user.supplierorderlist.add(sOrder)
    #     Pobj.supplierorderlist.add(sOrder)
    #     Sobj.supplierorderlist.add(sOrder)

    #     messages.info(request,'Commande Ajouté')
        
    #     return redirect('order_supplier_list')

    # else:
    #     productlist=request.user.productlist.all()
    #     supplierlist=request.user.supplierlist.all()
    #     Pcount= request.user.productlist.all().count()
    #     Ccount= request.user.clientlist.all().count()
    #     Scount= request.user.supplierlist.all().count()
    #     context= {
    #     "productlist": productlist,
    #     "supplierlist": supplierlist,
    #     "Pcount": Pcount,
    #     "Ccount": Ccount,
    #     "Scount": Scount
    #     }
    #     context.update(info(request))
    #     return render(request,"dashboard/order/order_supplier_create.html",context)

    OrderFormSet = inlineformset_factory( nSupplierOrder,nOrderS, fields = ('Product', 'Quantity',  ),extra= 10 )
    form = nSupplierOrderForm()
    form.fields['Supplier'].queryset = Supplier.objects.filter(user=request.user)
    form.fields['Supplier'].label = "Fournisseur"
    #oform = nOrderCForm() 
    formset = OrderFormSet()
    for ff in formset.forms:
        ff.fields['Product'].queryset = Product.objects.filter(user=request.user)
        ff.fields['Product'].label = "Produit"
        ff.fields['Quantity'].label = "Quantité"
    if request.method == "POST":
        
        form = nSupplierOrderForm(request.POST)
        if form.is_valid():
            nC=form.save()
            nC.Status = "en attente"
            formset = OrderFormSet(request.POST, instance = nC)
            if formset.is_valid():
                o = formset.save()
                tot=0
                for i in o:
                    tot=tot + (i.Quantity * i.Product.SalesPrice)
                nC.Total=tot
                nC.save()    
                request.user.nsupplierorderlist.add(nC)
                return redirect('order_supplier_list')
    else:
        productlist=request.user.productlist.all()
        clientlist=request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "productlist": productlist,
        "clientlist": clientlist,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        
        "formset": formset,
        "form"  : form
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_supplier_create.html",context)


def order_supplier_edittttt(request,id):
    obj = get_object_or_404(SupplierOrder, id=id)
    if request.method == 'POST':
        P = request.POST['product']
        Pobj = Product.objects.get(id=P)
        Pobj.save() 
        S = request.POST['supplier']
        Sobj = Supplier.objects.get(id=S)
        Sobj.save()


        Quantity = request.POST['quantity']
        Total = float(Quantity) * float(Pobj.PurchasePrice)
        Date = request.POST['date']
        Status = request.POST['status']
        error= False
        if not Product : 
            messages.info(request,'Le champ Produit ne peut pas etre vide')
            error=True
        if not Client : 
            messages.info(request,'Le champ Fournisseur  ne peut pas etre vide')
            error=True
        if not Quantity : 
            messages.info(request,'Le champ Quantité ne peut pas etre vide')
            error=True
        if not Date : 
            messages.info(request,'Le champ Date ne peut pas etre vide')
            error=True
        if not Status : 
            messages.info(request,'Le champ Etat ne peut pas etre vide')
            error=True
        if error:
            return redirect('order_supplier_edit',id)
        
        
        obj.Quantity = Quantity
        obj.Date = Date
        obj.Status = Status
        obj.Total = Total
        
        obj.save()
        
        request.user.supplierorderlist.add(obj)
        Pobj.supplierorderlist.add(obj)
        Sobj.supplierorderlist.add(obj)

        messages.info(request,'Commande Modifié')
        
        return redirect('order_supplier_list')

    else:
        
        productlist=request.user.productlist.all()
        supplierlist=request.user.supplierlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "productlist": productlist,
        "supplierlist": supplierlist,
        "obj": obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_supplier_edit.html",context)

def order_client_edittts(request,id):
    obj = get_object_or_404(ClientOrder, id=id)
    if request.method == 'POST':
        P = request.POST['product']
        Pobj = Product.objects.get(id=P)
        Pobj.save() 
        C = request.POST['client']
        Cobj = Client.objects.get(id=C)
        Cobj.save()


        Quantity = request.POST['quantity']
        Total = float(Quantity) * float(Pobj.SalesPrice)
        Date = request.POST['date']
        Status = request.POST['status']
        error= False
        if not Product : 
            messages.info(request,'Le champ Product ne peut pas etre vide')
            error=True
        if not Client : 
            messages.info(request,'Le champ Supplier  ne peut pas etre vide')
            error=True
        if not Quantity : 
            messages.info(request,'Le champ Quantity ne peut pas etre vide')
            error=True
        if not Date : 
            messages.info(request,'Le champ Date ne peut pas etre vide')
            error=True
        if not Status : 
            messages.info(request,'Le champ Status ne peut pas etre vide')
            error=True
        if error:
            return redirect('order_client_edit',id)
        
        
        obj.Quantity = Quantity
        obj.Date = Date
        obj.Status = Status
        obj.Total = Total
        
        obj.save()
        
        request.user.clientorderlist.add(obj)
        Pobj.clientorderlist.add(obj)
        Cobj.clientorderlist.add(obj)

        messages.info(request,'Commande Modifié')
        
        return redirect('order_client_list')

    else:
        
        productlist=request.user.productlist.all()
        clientlist=request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "productlist": productlist,
        "clientlist": clientlist,
        "obj": obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_edit.html",context)


def order_client_delete(request, id):
    obj=get_object_or_404(nClientOrder, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('order_client_list')
    else:
       
        list_clients= request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "obj":obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_clients" : list_clients
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_delete.html",context)
def order_supplier_deliver(request, id):

    order=get_object_or_404(nSupplierOrder, id=id)
    listorder = order.norderslist.all()
    for o in listorder : 
        o.Product.Quantity=o.Product.Quantity + o.Quantity
        o.Product.save()

    order.Status='livré'
    order.save()
    create_stock_track_supplier(request,order)
    messages.info(request,'Produit livré')
    return redirect('order_supplier_list')


def order_client_deliver(request, id):
    order=get_object_or_404(nClientOrder, id=id)
    listorder = order.norderclist.all()
    b = False
    for o in listorder : 
        if o.Quantity > o.Product.Quantity: 
            b = True   
    if b:
        return redirect('order_client_deliver_confirm',id=id)
    else:
        for o in listorder : 
            o.Product.Quantity=o.Product.Quantity-o.Quantity
            o.Product.save()
        order.Status='livré'
        order.save()
        create_stock_track_client(request,order) #zz
        messages.info(request,'Produit livré')
        return redirect('order_client_list')
       
def order_client_deliver_confirm(request, id):
    order=get_object_or_404(nClientOrder, id=id)
    listorder = order.norderclist.all()
    if request.method == "POST":
        create_stock_track_client_confirm(request,order)
        listorder = order.norderclist.all()
        for o in listorder : 
            o.Product.Quantity=o.Product.Quantity-o.Quantity
            o.Product.save()
        
        order.Status='livré'
        order.save()
        
        return redirect('order_client_list')
    else:
        list_clients= request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "obj":order,
        "listorder":listorder,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_clients" : list_clients
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_deliver_confirm.html",context)
       
def order_supplier_delete(request, id):
    obj=get_object_or_404(nSupplierOrder, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('order_supplier_list')
    else:
       
        list_clients= request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "obj":obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_clients" : list_clients
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_supplier_delete.html",context)


def contact(request):
    return render(request,"contact.html",{})

def about(request):
    return render(request,"about.html",{})

def services(request):
    return render(request,"services.html",{})

def learnmore(request):
    return render(request,"learnmore.html",{})


def order_client_create(request):
    OrderFormSet = inlineformset_factory( nClientOrder,nOrderC, fields = ('Product', 'Quantity',  ),extra= 10 )
    form = nClientOrderForm()
    #oform = nOrderCForm() 
    formset = OrderFormSet()
    form.fields['Client'].queryset = Client.objects.filter(user=request.user)
    for ff in formset.forms:
        ff.fields['Product'].queryset = Product.objects.filter(user=request.user)
        ff.fields['Product'].label = "Produit"
        ff.fields['Quantity'].label = "Quantité"
    if request.method == "POST":
        form = nClientOrderForm(request.POST)
        if form.is_valid():
            nC=form.save()
            nC.Status = "en attente"
            formset = OrderFormSet(request.POST, instance = nC)
            if formset.is_valid():
                o = formset.save()
                tot=0
                for i in o:
                    tot=tot + (i.Quantity * i.Product.SalesPrice)
                nC.Total=tot
                nC.save()    
                request.user.nclientorderlist.add(nC)
                return redirect('order_client_list')
    else:
        productlist=request.user.productlist.all()
        clientlist=request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "productlist": productlist,
        "clientlist": clientlist,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        
        "formset": formset,
        "form"  : form
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_create.html",context)

def order_client_details(request, id):  
    obj=get_object_or_404(nClientOrder, id=id)
    if request.method == "POST":
        if 'xls' in request.POST: 

            output = io.BytesIO()

            workbook = Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, "Client")
            worksheet.write(0, 1, str(obj.Client))
            worksheet.write(1, 0, "Date")
            worksheet.write(1, 1, str(obj.Date))
            worksheet.write(2, 0, "Etat")
            worksheet.write(2, 1, str(obj.Status))
            worksheet.write(4, 0, "Produit")
            worksheet.write(4, 1, "Prix")
            worksheet.write(4, 2, "Quantité")
            worksheet.write(4, 3, "Total")

            i=5
            for o in obj.norderclist.all():
                #writer.writerow([o.Product,o.Product.SalesPrice,o.Quantity,o.line_total() ])
                worksheet.write(i, 0, str(o.Product))
                worksheet.write(i, 1, o.Product.SalesPrice)
                worksheet.write(i, 2, o.Quantity)
                worksheet.write(i, 3, o.line_total())
                i=i+1
            worksheet.write(i, 2, "Grand Total")
            worksheet.write(i, 3, obj.Total)
            workbook.close()

            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")            
            filen = str(obj.Client) + " " + str(obj.Date) + ".xlsx"
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filen)

            output.close()
            return response
        if 'pdf' in request.POST: 
            context = {
                "obj" : obj
            }

            return render_to_pdf("other/order_client_detail.html",context)
    else: 
        list_clients= request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "obj":obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
    
        "list_clients" : list_clients
        }
        context.update(info(request))
        
        return render(request,"dashboard/order/order_client_details.html",context)
    

def order_supplier_details(request, id): 
    obj=get_object_or_404(nSupplierOrder , id=id)
    if request.method == "POST":
        if 'xls' in request.POST: 
            output = io.BytesIO()
            workbook = Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, "Fournisseur")
            worksheet.write(0, 1, str(obj.Supplier))
            worksheet.write(1, 0, "Date")
            worksheet.write(1, 1, str(obj.Date))
            worksheet.write(2, 0, "Etat")
            worksheet.write(2, 1, str(obj.Status))
            worksheet.write(4, 0, "Produit")
            worksheet.write(4, 1, "Prix")
            worksheet.write(4, 2, "Quantité")
            worksheet.write(4, 3, "Total")
            i=5
            for o in obj.norderslist.all():
                #writer.writerow([o.Product,o.Product.SalesPrice,o.Quantity,o.line_total() ])
                worksheet.write(i, 0, str(o.Product))
                worksheet.write(i, 1, o.Product.PurchasePrice)
                worksheet.write(i, 2, o.Quantity)
                worksheet.write(i, 3, o.line_total())
                i=i+1
            worksheet.write(i, 2, "Grand Total")
            worksheet.write(i, 3, obj.Total)
            workbook.close()

            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")            
            filen = str(obj.Supplier) + " " + str(obj.Date) + ".xlsx"
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filen)
            output.close()
            return response
        if 'pdf' in request.POST: 
            context = {
                "obj" : obj
            }

            return render_to_pdf("other/order_supplier_detail.html",context)
    else:   
        list_clients= request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "obj":obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
    
        "list_clients" : list_clients
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_supplier_details.html",context)



def order_client_edit(request,id):
    obj = get_object_or_404(nClientOrder, id=id)
    
    OrderFormSet = inlineformset_factory( nClientOrder,nOrderC, fields = ('Product', 'Quantity',  ),extra= 10 )
    form = nClientOrderForm(instance=obj)
    formset = OrderFormSet()
    for ff in formset.forms:
        ff.fields['Product'].queryset = Product.objects.filter(user=request.user)
        ff.fields['Product'].label = "Produit"
        ff.fields['Quantity'].label = "Quantité"
        
    
    if request.method == 'POST':
        Status = request.POST['status']
        form = nClientOrderForm(request.POST,instance= obj)
        if form.is_valid():
            nC=form.save()
            nC.Status = Status
            formset = OrderFormSet(request.POST, instance = nC)

            if formset.is_valid():
                #delete older orders before updating
                o = obj.norderclist.all()
                for ob in o:
                    ob.delete()
                formset.save()
                o = obj.norderclist.all()
                tot=0
                for i in o:
                    tot=tot + (i.Quantity * i.Product.SalesPrice)
                nC.Total=tot
                nC.save()    
                request.user.nclientorderlist.add(nC)
                return redirect('order_client_list')
    else:
        
        productlist=request.user.productlist.all()
        clientlist=request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "productlist": productlist,
        "clientlist": clientlist,
        "obj": obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "form": form,
        "formset": formset,
        "Scount": Scount
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_edit.html",context)

def order_supplier_edit(request,id):
    obj = get_object_or_404(nSupplierOrder, id=id)
    OrderFormSet = inlineformset_factory( nSupplierOrder,nOrderS, fields = ('Product', 'Quantity',  ),extra= 10 )
    form = nSupplierOrderForm(instance=obj)
    formset = OrderFormSet()
    form.fields['Supplier'].queryset = Supplier.objects.filter(user=request.user)
    form.fields['Supplier'].label = "Fournisseur"
    for ff in formset.forms:
        ff.fields['Product'].queryset = Product.objects.filter(user=request.user)
        ff.fields['Product'].label = "Produit"
        ff.fields['Quantity'].label = "Quantité"
    if request.method == 'POST': 
        Status = request.POST['status']
        form = nSupplierOrderForm(request.POST,instance= obj)
        if form.is_valid():
            nC=form.save()
            nC.Status = Status
            formset = OrderFormSet(request.POST, instance = nC)
            
            if formset.is_valid():
                
                #delete older orders before updating
                o = obj.norderslist.all()
                for ob in o:
                    ob.delete()
                formset.save()
                o = obj.norderslist.all()
                tot=0
                for i in o:
                    tot=tot + (i.Quantity * i.Product.SalesPrice)
                nC.Total=tot
                nC.save()    
                request.user.nsupplierorderlist.add(nC)
                return redirect('order_supplier_list')
            
    else: 
        productlist=request.user.productlist.all()
        clientlist=request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "productlist": productlist,
        "clientlist": clientlist,
        "obj": obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "form": form,
        "formset": formset,
        "Scount": Scount
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_supplier_edit.html",context)