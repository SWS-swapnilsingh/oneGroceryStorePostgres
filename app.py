from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

# ========================== database details =================================
database="test"
user="postgres"
password="qazwsx"
host="127.0.0.1"
port="5432"

# ========================= Configuration ===============================================
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
app.config['SQLALCHEMY_DATABASE_URI'] = url
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

# =============================== Models =======================================

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    category_name = db.Column(db.String(), unique = True, nullable = False)
    all_product = db.relationship('Product', backref = "all_category", secondary = "category_product")

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    product_name = db.Column(db.String(),unique = True, nullable = False)
    price_unit = db.Column(db.Integer(), nullable = False)
    unit = db.Column(db.String(), nullable = False)
    manufac_date = db.Column(db.String(),unique = False, nullable = False)
    exp_date = db.Column(db.String(),unique = False, nullable = False)
    quantity = db.Column(db.Integer(), unique = False, nullable = False)
    discount = db.Column(db.Integer(), nullable = False)

class DiscountCoupon(db.Model):
    __tablename__ = 'discountcoupon'
    coupon_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    product_code = db.Column(db.String(),unique = True, nullable = False)

class Category_product(db.Model):
    __tablename__ = 'category_product'
    cp_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    cp_category_id = db.Column(db.Integer(), db.ForeignKey("category.category_id"), nullable = False)
    cp_product_id = db.Column(db.Integer(), db.ForeignKey("product.product_id"), nullable = False)

class Login(db.Model):
    __tablename__ = 'login'
    login_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    username = db.Column(db.String(),unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    position = db.Column(db.String(), nullable = False)

# ================================= Controllers ===================================

# @app.route('/', methods = ['GET','POST'])
# def delete():
#     # deleting category1
#     c1 = Category.query.get(1)
#     print(c1)

#     # deleting all product related to that category
#     all_p = c1.all_product
#     print(all_p)

#     for p_obj in all_p:
#         db.session.delete(p_obj)
#         db.session.commit()
    
#     # deleting all the category product relation for that category
#     cp1 = Category_product.query.filter_by(cp_category_id = c1.category_id).all()
#     print(cp1)

#     for cp in cp1:
#         db.session.delete(cp)
#         db.session.commit()
    
#     db.session.delete(c1)
#     db.session.commit()

#     return '<h1> deleted </h1>'

@app.route('/', methods  = ['GET', 'POST'])
def loginPage():
    return render_template('loginpage.html')

@app.route('/loginmanager', methods = ['GET','POST'])
def loginmanger():
    if request.method == 'GET':
        return render_template('loginmanagerform.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # print('===============================================')
        # print(username, password)
        # position = 'manager'
        position = request.form.get('position')

        #validating user input
        if '@' not in username:
            return '<h1> Username must contain "@".</h1><br><a href="/loginmanager">Back</a>'
        
        #validating password
        
        # converting password into list
        passwordlist = list(password)
        
        #capital alphabet list
        c_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        c_alphalist = list(c_alpha)

        #small alphabet list
        s_alpha = 'abcdefghijklmnopqrstuvwxyz'
        s_alphalist = list(s_alpha)

        #special symbol list
        symbol = '@#$&*'
        symbollist = list(symbol)

        #number list
        num = '0123456789'
        numlist = list(num)

        capital_alphabet = False
        small_alphabet = False
        symb = False
        number = False
        for a in password:
            if a in c_alphalist:
                capital_alphabet = True
            if a in s_alphalist:
                small_alphabet = True
            if a in symbollist:
                symb = True
            if a in numlist:
                number = True
        
        if capital_alphabet == False or small_alphabet == False or symb == False or number == False:
            return '<h1> Password must contain atleast one Capital Alphabet, Small Alphabet, Number and symbol "@,#,$,&,*".</h1><br><a href="/loginmanager">Back</a>'

        l1 = Login.query.filter(Login.username == username, Login.password == password, Login.position == position).first()

        # print(l1)
        if l1 is not None:
            # return redirect('/manager_view')
            # return redirect('/managerhomepage')
            if l1.position == 'manager':
                return redirect('/managerhomepage')
            elif l1.position == 'user':
                return redirect('/homepage')

        elif l1 is None:
            return '<h1> username or password not matched</h1><br><a href="/">Login Page</a>'
        
# manager homepage where all the categories and items are listed
@app.route('/managerhomepage', methods = ['GET', 'POST'])
def managerHomePage():
    c1 = Category.query.all()
    p1 = Product.query.all()

    return render_template('landingpageofmanager.html', c1=c1, p1=p1)

@app.route('/loginuser', methods = ['GET', 'POST'])
def loginuser():
    if request.method == 'GET':
        return render_template('loginuserform.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # print('===============================================')
        # print(username, password)

        #validating user input
        if '@' not in username:
            return '<h1> Username must contain "@".</h1><br><a href="/loginuser">Back</a>'
        
        #validating password

        # converting password into list
        passwordlist = list(password)
        
        #capital alphabet list
        c_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        c_alphalist = list(c_alpha)

        #small alphabet list
        s_alpha = 'abcdefghijklmnopqrstuvwxyz'
        s_alphalist = list(s_alpha)

        #special symbol list
        symbol = '@#$&*'
        symbollist = list(symbol)

        #number list
        num = '0123456789'
        numlist = list(num)

        capital_alphabet = False
        small_alphabet = False
        symb = False
        number = False
        for a in password:
            if a in c_alphalist:
                capital_alphabet = True
            if a in s_alphalist:
                small_alphabet = True
            if a in symbollist:
                symb = True
            if a in numlist:
                number = True
        
        if capital_alphabet == False or small_alphabet == False or symb == False or number == False:
            return '<h1> Password must contain atleast one Capital Alphabet, Small Alphabet, Number and symbol "@,#,$,&,*".</h1><br><a href="/loginuser">Back</a>'

        position = 'user'

        l1 = Login.query.filter(Login.username == username, Login.password == password, Login.position == position).first()

        # print(l1)
        if l1 is not None:
            # c1 = Category.query.all()
            # p1 = Product.query.all()
            # return redirect('/manager_view')
            # return '<h1>user view</h1>'
            return redirect('/homepage')
        elif l1 is None:
            return '<h1> username or password not matched</h1><br><a href="/">Login Page</a>'

# homepage where all the categories and items are listed
@app.route('/homepage', methods = ['GET', 'POST'])
def homePage():
    c1 = Category.query.all()
    p1 = Product.query.all()

    return render_template('landingpageofuser.html', c1=c1, p1=p1)


#User registration
@app.route('/userregistration', methods= ['GET','POST'])
def userregistration():
    if request.method == 'GET':
        return render_template('userregistration.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #validating user input
        if '@' not in username:
            return '<h1> Username must contain "@".</h1><br><a href="/userregistration">Back</a>'
        
        #validating password

        # converting password into list
        passwordlist = list(password)
        
        #capital alphabet list
        c_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        c_alphalist = list(c_alpha)

        #small alphabet list
        s_alpha = 'abcdefghijklmnopqrstuvwxyz'
        s_alphalist = list(s_alpha)

        #special symbol list
        symbol = '@#$&*'
        symbollist = list(symbol)

        #number list
        num = '0123456789'
        numlist = list(num)

        capital_alphabet = False
        small_alphabet = False
        symb = False
        number = False
        for a in password:
            if a in c_alphalist:
                capital_alphabet = True
            if a in s_alphalist:
                small_alphabet = True
            if a in symbollist:
                symb = True
            if a in numlist:
                number = True
        
        if capital_alphabet == False or small_alphabet == False or symb == False or number == False:
            return '<h1> Password must contain atleast one Capital Alphabet, Small Alphabet, Number and symbol "@,#,$,&,*".</h1><br><a href="/userregistration">Back</a>'

        #checking whether the new username is unique or not
        cl1 = Login.query.filter(Login.username == username).first()
        if cl1 is not None:
            return '<h1> this username already exists</h1><br><a href="/">Login Page</a>'
        if cl1 is None:

            position = 'user'

            l1 = Login(username = username, password = password, position=position)
            db.session.add(l1)
            db.session.commit()

            return '<h1> successfuly registered as user </h1><br><a href="/">Login Page</a>'

#Manager registration
@app.route('/managerregistration', methods= ['GET','POST'])
def managerregistration():
    if request.method == 'GET':
        return render_template('managerregistration.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        companycode = request.form.get('companycode')

        #authenticating company code
        if companycode != '123456':
            return '<h1> company code not matched </h1><br><a href="/">Login Page</a>'
        
        #validating user input
        if '@' not in username:
            return '<h1> Username must contain "@".</h1><br><a href="/managerregistration">Back</a>'
        
        #validating password
        
        # converting password into list
        passwordlist = list(password)
        
        #capital alphabet list
        c_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        c_alphalist = list(c_alpha)

        #small alphabet list
        s_alpha = 'abcdefghijklmnopqrstuvwxyz'
        s_alphalist = list(s_alpha)

        #special symbol list
        symbol = '@#$&*'
        symbollist = list(symbol)

        #number list
        num = '0123456789'
        numlist = list(num)

        capital_alphabet = False
        small_alphabet = False
        symb = False
        number = False
        for a in password:
            if a in c_alphalist:
                capital_alphabet = True
            if a in s_alphalist:
                small_alphabet = True
            if a in symbollist:
                symb = True
            if a in numlist:
                number = True
        
        if capital_alphabet == False or small_alphabet == False or symb == False or number == False:
            return '<h1> Password must contain atleast one Capital Alphabet, Small Alphabet, Number and symbol "@,#,$,&,*".</h1><br><a href="/managerregistration">Back</a>'

        #checking whether the new username is unique or not
        cl1 = Login.query.filter(Login.username == username).first()
        if cl1 is not None:
            return '<h1> this username already exists</h1><br><a href="/">Login Page</a>'
        if cl1 is None:

            position = 'manager'

            l1 = Login(username = username, password = password, position=position)
            db.session.add(l1)
            db.session.commit()

            return '<h1> successfuly registered as manager </h1><br><a href="/">Login Page</a>'

#add category
@app.route('/addcategory', methods = ['GET','POST'])
def addCategory():
    if request.method == 'GET':
        return render_template('addcategory.html')
    if request.method == 'POST':
        categoryname = request.form.get('categoryname')

        #validatiion for category name
        categoryname_list = categoryname.split()
        for name in categoryname_list:
            if name.isalpha() == False:
                return f'<h1> All characters of category name should be alphabet.</h1><br><a href="/addcategory">Back</a>'

        #check already this category name exist or not
        c1 = Category.query.filter(Category.category_name == categoryname).first()

        if c1 is not None:
            return '<h1> this category name already exists </h1><br><a href="/addcategory">Back</a>'
        if c1 is None:
            nc1 = Category(category_name = categoryname)
            db.session.add(nc1)
            db.session.commit()

            return redirect('/managerhomepage')
                
#add product
@app.route('/addproduct/<int:categoryId>', methods = ['GET','POST'])
def addProduct(categoryId):
    categoryId = int(categoryId)
    if request.method == 'GET':
        return render_template('addproduct.html', categoryId=categoryId)
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        price_unit = request.form.get('price_unit')
        # price_unit = int(price_unit)
        unit = request.form.get('unit')
        manufac_year = request.form.get('manufac_year')
        exp_year = request.form.get('exp_year')
        qty = request.form.get('qty')
        # qty = int(qty)
        discount = request.form.get('discount')
        # discount = int(discount)

        #validation

        #validatiion for product name
        product_name_list = product_name.split()
        for name in product_name_list:
            if name.isalpha() == False:
                return f'<h1> All characters of product name should be alphabet.</h1><br><a href="/addproduct/{categoryId}">Back</a>'


        if price_unit.isdigit() == False:
            return f'<h1> Price should be a integer value.</h1><br><a href="/addproduct/{categoryId}">Back</a>'
        if unit.isalpha() == False:
            return f'<h1> All characters of unit should be alphabet.</h1><br><a href="/addproduct/{categoryId}">Back</a>'
        if qty.isdigit() == False:
            return f'<h1> Quantity should be a integer value.</h1><br><a href="/addproduct/{categoryId}">Back</a>'
        if discount.isdigit() == False:
            return f'<h1> Discount should be a integer value.</h1><br><a href="/addproduct/{categoryId}">Back</a>'
        
        #validation for date
        if len(manufac_year) != 10:
            return f'<h1> Manufacture date should be of "dd/mm/yyyy" format.</h1><br><a href="/addproduct/{categoryId}">Back</a>'
        m_dd = manufac_year[:2]
        m_separater1 = manufac_year[2:3]
        m_mm = manufac_year[3:5]
        m_separater2 = manufac_year[5:6]
        m_yyyy = manufac_year[6:]

        if len(exp_year) != 10:
            return f'<h1> Expiry date should be of "dd/mm/yyyy" format.</h1><br><a href="/addproduct/{categoryId}">Back</a>'
        e_dd = exp_year[:2]
        e_separater1 = exp_year[2:3]
        e_mm = exp_year[3:5]
        e_separater2 = exp_year[5:6]
        e_yyyy = exp_year[6:]

        if m_dd.isdigit() == False or m_separater1 != '/' or m_mm.isdigit() == False or m_separater2 != '/' or m_yyyy.isdigit() == False:
            return f'<h1> Manufacture date should be of "dd/mm/yyyy" format.</h1><br><a href="/addproduct/{categoryId}">Back</a>'
        if e_dd.isdigit() == False or e_separater1 != '/' or e_mm.isdigit() == False or e_separater2 != '/' or e_yyyy.isdigit() == False:
            return f'<h1> Expiry date should be of "dd/mm/yyyy" format.</h1><br><a href="/addproduct/{categoryId}">Back</a>'

        
        #type casting
        price_unit = int(price_unit)
        qty = int(qty)
        discount = int(discount)




        #checking if this product name already exists or not
        cp1 = Product.query.filter(Product.product_name == product_name).first()
        if cp1 is not None:
            return f'<h1> this product name already exists</h1><br><a href="/addproduct/{categoryId}">Back</a>'
        if cp1 is None:

            #adding new product to the product table
            p1 = Product(product_name = product_name, price_unit=price_unit, unit=unit, manufac_date = manufac_year, exp_date = exp_year, quantity=qty, discount=discount)
            db.session.add(p1)
            db.session.commit()

            #adding category-product relation inside categoryProduct table
            # c1 = Category.query.get(categoryId)
            p1_ = Product.query.filter(Product.product_name == product_name).first()

            cp1 = Category_product(cp_category_id = categoryId, cp_product_id = p1_.product_id)
            db.session.add(cp1)
            db.session.commit()

            return redirect('/managerhomepage')

# add product from manager landingpage
@app.route('/addproduct_from_manager_landingpage', methods=['GET', 'POST'])
def addProductFromManagerLandingPage():
    if request.method == 'GET':
        return render_template('addProductFromManagerLandingPage.html')
    if request.method == 'POST':
        category_name = request.form.get('category_name')

        c1 = Category.query.filter(Category.category_name == category_name).first()
        if c1 is None:
            return '<h1> This category does not exist</h1><br><a href="/addproduct_from_manager_landingpage">Back</a>'
        if c1 is not None:
            cid = c1.category_id
            url = f'/addproduct/{cid}'
            return redirect(url)

        

# #show all category
# @app.route('/', methods=['GET', 'POST'])
# def allCategory():

#     c1 = Category.query.all()
#     p1 = Product.query.all()

#     return render_template('base.html', c1=c1, p1=p1)



# validation before deleting a category
@app.route('/reallydeletecategory', methods = ['GET', 'POST'] )
def reallyDeleteCategory():
    if request.method == 'GET':
        return render_template('reallydeletecategory.html')
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        c1 = Category.query.filter(Category.category_name == category_name).first()
        if c1 is None:
            return '<h1>incorrect category name</h1><br><a href="/reallydeletecategory">Back</a>'
        if c1 is not None:
            cid = c1.category_id
            # db.session.delete(p1)
            # db.session.commit()
            url = f'/deletecategory/{cid}'
            return redirect(url)


#delete a category
@app.route('/deletecategory/<int:categoryId>', methods=['GET', 'POST'])
def deleteCategory(categoryId):
    categoryId = int(categoryId)

    c1 = Category.query.get(categoryId)
    if c1 is None:
        return f'<h1>this category already deleted</h1><br><a href="/deletecategory/{categoryId}">Back</a>'
    if c1 is not None:

        allprod = c1.all_product
        print(allprod)

        #deleting all the product belonging to this category
        for prod in allprod:
            db.session.delete(prod)
            db.session.commit()
        
        #deleting all the category product relation from category product table
        cp1 = Category_product.query.filter(Category_product.cp_category_id == categoryId).all()
        for cp in cp1:
            db.session.delete(cp)
            db.session.commit()
        
        db.session.delete(c1)
        db.session.commit()

        return redirect('/managerhomepage')

#validation before deleting a product
@app.route('/really', methods = ['GET', 'POST'] )
def really():
    if request.method == 'GET':
        return render_template('really.html')
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        p1 = Product.query.filter(Product.product_name == product_name).first()
        if p1 is None:
            return '<h1>incorrect product name</h1><br><a href="/really">Back</a>'
        if p1 is not None:
            pid = p1.product_id
            # db.session.delete(p1)
            # db.session.commit()
            url = f'/deleteproduct/{pid}/0'
            return redirect(url)


#delete a product
# check == 0 //from home page
# check == 1 // from perticular category page
@app.route('/deleteproduct/<int:productId>/<int:check>', methods =['GET', 'POST'])
def deleteProduct(productId, check):
    productId = int(productId)
    check = int(check)

    p1 = Product.query.get(productId)
    if p1 is None:
        return f'<h1>this product does not exist</h1><br><a href="/deleteproduct/{productId}/{check}">Back</a>'
    if p1 is not None:

        #finding corresponding category of the product
        # c1 = p1.all_category
        # print(c1,"**********************************************")
        # c = c1[0]
        # print(c,"**********************************************")

        #deleting all the relation from category product table belonging to this product
        cp1 = Category_product.query.filter(Category_product.cp_product_id == productId).all()
        for cp in cp1:
            db.session.delete(cp)
            db.session.commit()

        db.session.delete(p1)
        db.session.commit()

        # if check == 0:
        return redirect('/managerhomepage')
        # if check == 1:
        #     # c = c[0]
        #     # print(c)
        #     cid = c.category_id

        #     url = f'/managereachcategory/{cid}'
        #     return redirect(url)
        #     # return '<h1>deleted successfully</h1>'

buyingproduct = []
# this route is for, when somebody click on the perticular category in a sidebar
@app.route('/eachcategory/<int:categoryId>', methods = ['GET', 'POST'])
def eachCategory(categoryId):
    category_id = int(categoryId)
    c = Category.query.get(category_id)
    ap1 = c.all_product

    c1 = Category.query.all()
    
    if ap1 == []:
        return f'<h1>No product in this category</h1><br><a href="/homepage">Back</a>'
    elif ap1 is not None:
        return render_template('eachcategory.html', c1=c1, p1=ap1, perticular_c=c)

#manager's eachcategory
@app.route('/managereachcategory/<int:categoryId>', methods = ['GET', 'POST'])
def managereachCategory(categoryId):
    category_id = int(categoryId)
    c = Category.query.get(category_id)
    ap1 = c.all_product

    c1 = Category.query.all()
    
    if ap1 == []:
        return render_template('managereachcategory.html', c1=c1, p1=ap1, perticular_c=c)
    elif ap1 is not None:
        return render_template('managereachcategory.html', c1=c1, p1=ap1, perticular_c=c)

#jabbhi koi add button par click karega homepage to yha par aayega
@app.route('/buyinglist/<int:productId>', methods = ['GET', 'POST'])
def buyingList(productId):
    global buyingproduct
    product_id = int(productId)
    p = Product.query.get(product_id)
    if p.quantity <= 0:
        return '<h1>Out of stock</h1>'
    else:
        buyingproduct.append(p)    
        # return render_template('cart.html', buyingproduct=buyingproduct)
        return redirect('/homepage')

#jabbhi koi add button par click karega perticular category page to yha par aayega
@app.route('/buying/<int:productId>/<int:categoryId>', methods= ['GET', 'POST'])
def eachCategoryBuying(productId, categoryId):
    categoryId = int(categoryId)
    product_id = int(productId)

    global buyingproduct
    p = Product.query.get(product_id)
    if p.quantity <= 0:
        return '<h1>Out of stock</h1>'
    else:
        buyingproduct.append(p)
        url = f'/eachcategory/{categoryId}'
        # print(buyingproduct)
        return redirect(url)

# cart
@app.route('/cart', methods = ['GET', 'POST'])
def cart():
    if len(buyingproduct) == 0:
        return '<h1> Empty Cart</h1><br><a href="/homepage">Home</a>'
    totalamt = 0
    for p in buyingproduct:
        totalamt += p.price_unit

    return render_template('cart.html', buyingproduct = buyingproduct, totalamt = totalamt)


# cart with discount coupon
# @app.route('/cartdiscountcoupon', methods = ['GET', 'POST'])
# def cartDiscountCoupon():
#     if len(buyingproduct) == 0:
#         return '<h1> Empty Cart</h1><br><a href="/homepage">Home</a>'
#     totalamt = 0
#     for p in buyingproduct:
#         totalamt += p.price_unit
    
#     discount_coupon = request.form.get('discountcoupon')

#     return render_template('cart.html', buyingproduct = buyingproduct, totalamt = totalamt)



# #manager add coupon
# @app.route('/manager_add_coupon', methods=['GET', 'POST'])
# def managerAddCoupon():
#     if request.method == 'GET':
#         return render_template('managerAddCoupon.html')
#     if request.method == 'POST':
#         couponCode = request.form.get('couponCode')

#         #validation
#         if couponCode.isalnum() == False:
#             return '<h1> Coupon Code must be alpha numeric.</h1>'
#         if len(couponCode) == 5:
#             return '<h1> Length of coupon code must be 5.</h1>'
        




# delete items from cart
@app.route('/deleteitemsfromcart/<int:pid>', methods=['GET', 'POST'])
def deleteItemsFromCart(pid):
    global buyingproduct
    productId = int(pid)
    p1 = Product.query.get(productId)
    print(p1)
    # print(p1 in buyingproduct)
    new_buyingproduct = []
    for p in buyingproduct:
        if p.product_id == productId:
            pass
        else:
            new_buyingproduct.append(p)
    
    buyingproduct = new_buyingproduct

    # buyingproduct.remove(p1)
    print(buyingproduct)
    return redirect('/cart')



#buy
@app.route('/buy', methods = ['GET', 'POST'])
def buy():
    global buyingproduct
    # reducing the qty of each bought item
    for p_ in buyingproduct:
        # print('product quantity', p.quantity , p.product_name)
        # a = p.quantity
        # a = a-1
        # p.quantity = a
        p1 = Product.query.get(p_.product_id)
        if p1.quantity <= 0:
            buyingproduct = []
            productname = p1.product_name
            return f'<h1>SORRY, {productname} is out of stock</h1><br><a href="/homepage">Home</a>'
        p1.quantity -= 1
        db.session.commit()
        # print(p1.quantity,'*********************************')
    buyingproduct = []

    return '<h1>Congratulations!! &nbsp;  Your order is placed </h1><br><a href="/homepage">Home</a>'

#search
@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    if request.method == 'POST':
        item = request.form.get('item')

        # print('itemproduct:', itemproduct)
        # print('itemcategory:', itemcategory, itemcategory == '')
        c1 = Category.query.all()

        
        p1 = Product.query.filter(Product.product_name == item).all()

        if len(p1) == 0:
            return '<h1> No such product </h1><br><a href="/search">Back</a>'
        
            
            
        return render_template('landingpageofuser.html', c1=c1, p1=p1)

#search perticular category
@app.route('/searchperticularcategory', methods = ['GET', 'POST'])
def searchPerticularCategory():
    c_name = request.form.get('item')
    c1 = Category.query.filter(Category.category_name == c_name).first()
    if c1 is None:
        return '<h1> This category does not exist</h1><a href="/search">Back</a>'
    if c1 is not None:
        cid = c1.category_id
        # url = f'/eachcategory/{cid}'
        return f'<h1> Category Found </h1><br><a href="/eachcategory/{cid}">see all its items</a>'

#manager search
@app.route('/managersearch', methods = ['GET', 'POST'])
def managersearch():
    if request.method == 'GET':
        return render_template('managersearch.html')
    if request.method == 'POST':
        item = request.form.get('item')

        # print('itemproduct:', itemproduct)
        # print('itemcategory:', itemcategory, itemcategory == '')
        c1 = Category.query.all()

        
        p1 = Product.query.filter(Product.product_name == item).all()

        if len(p1) == 0:
            return '<h1> No such product </h1><br><a href="/managersearch">Back</a>'
        
            
            
        return render_template('landingpageofmanager.html', c1=c1, p1=p1)

#manager search perticular category
@app.route('/managersearchperticularcategory', methods = ['GET', 'POST'])
def managerSearchPerticularCategory():
    c_name = request.form.get('item')
    c1 = Category.query.filter(Category.category_name == c_name).first()
    if c1 is None:
        return '<h1> This category does not exist</h1><a href="/managersearch">Back</a>'
    if c1 is not None:
        cid = c1.category_id
        # url = f'/eachcategory/{cid}'
        return f'<h1> Category Found </h1><br><a href="/managereachcategory/{cid}">see all its items</a>'

#filter each category for user
@app.route('/searcheachcategory/<int:categoryId>', methods = ['GET', 'POST'])
def searchEachCategory(categoryId):
    category_id = int(categoryId)
    c = Category.query.get(category_id)
    ap1 = c.all_product

    start = request.form.get('start')
    upto = request.form.get('upto')
    # print(type(start),'***************************8')
    # print(type(upto))

    filtered_ap1 = []
    for p in ap1:
        if int(start) <= p.price_unit <= int(upto):
            filtered_ap1.append(p)


    c1 = Category.query.all()
    
    if filtered_ap1 == []:
        return f'<h1>No Product In This Range</h1><br><a href="/homepage">Home</a>'
    elif filtered_ap1 is not None:
        return render_template('eachcategory.html', c1=c1, p1=filtered_ap1, perticular_c=c)
    
#filter each category for manager
@app.route('/managersearcheachcategory/<int:categoryId>', methods = ['GET', 'POST'])
def managersearchEachCategory(categoryId):
    category_id = int(categoryId)
    c = Category.query.get(category_id)
    ap1 = c.all_product

    start = request.form.get('start')
    upto = request.form.get('upto')
    # print(type(start),'***************************8')
    # print(type(upto))

    filtered_ap1 = []
    for p in ap1:
        if int(start) <= p.price_unit <= int(upto):
            filtered_ap1.append(p)


    c1 = Category.query.all()
    
    if filtered_ap1 == []:
        return f'<h1>No Product In This Range</h1><br><a href="/homepage">Home</a>'
    elif filtered_ap1 is not None:
        return render_template('managereachcategory.html', c1=c1, p1=filtered_ap1, perticular_c=c)


# overall filter - filter from homepage for user
@app.route('/overallfilter', methods = ['GET', 'POST'])
def overAllFilter():
    start = request.form.get('start')
    upto = request.form.get('upto')

    c1 = Category.query.all()
    p1 = Product.query.all()

    filtered_p1 = []
    for p in p1:
        if int(start) <= p.price_unit <= int(upto):
            filtered_p1.append(p)
    
    if filtered_p1 == []:
        return '<h1>No Product In This Range</h1><br><a href="/managerhomepage">Home</a>'
    elif filtered_p1 is not None:
        return render_template('landingpageofuser.html', c1=c1, p1=filtered_p1)


# overall filter - filter from homepage for manager
@app.route('/manageroverallfilter', methods = ['GET', 'POST'])
def manageroverAllFilter():
    start = request.form.get('start')
    upto = request.form.get('upto')

    c1 = Category.query.all()
    p1 = Product.query.all()

    filtered_p1 = []
    for p in p1:
        if int(start) <= p.price_unit <= int(upto):
            filtered_p1.append(p)
    
    if filtered_p1 == []:
        return '<h1>No Product In This Range</h1><br><a href="/managerhomepage">Home</a>'
    elif filtered_p1 is not None:
        return render_template('landingpageofmanager.html', c1=c1, p1=filtered_p1)
     

#update category
@app.route('/updatecategory/<int:categoryId>', methods = ['GET', 'POST'])
def updateCategory(categoryId):
    categoryId = int(categoryId)
    if request.method == 'GET':
        return render_template('updatecategory.html', categoryId=categoryId)
    if request.method == 'POST':
        newcategoryname = request.form.get('newcategoryname')
        c1 = Category.query.get(categoryId)
        c1.category_name = newcategoryname
        db.session.commit()
    return redirect('/managerhomepage')

# update product
@app.route('/updateproduct/<int:productId>', methods = ['GET', 'POST'])
def updateProduct(productId):
    productId = int(productId)
    p = Product.query.get(productId)
    if request.method == 'GET':
        return render_template('updateproduct.html', p = p)
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        price_unit = request.form.get('price_unit')
        price_unit = int(price_unit)
        unit = request.form.get('unit')
        manufac_year = request.form.get('manufac_year')
        exp_year = request.form.get('exp_year')
        qty = request.form.get('qty')
        qty = int(qty)
        discount = request.form.get('discount')
        discount = int(discount)

        p.product_name =product_name
        p.price_unit = price_unit
        p.unit = unit
        p.manufac_date = manufac_year
        p.exp_date = exp_year
        p.quantity = qty
        p.discount = discount

        db.session.commit()
        return redirect('/managerhomepage')



@app.route('/bargraph', methods=['GET','POST'])
def barGraph():
    # creating the dataset
    # data = {'C':20, 'C++':15, 'Java':30,
    #         'Python':35}
    # courses = list(data.keys())
    # values = list(data.values())
    p1 = Product.query.all()
    # productnames=[]
    # quantitylist=[]
    # for p in p1:
        # productnames.append(p.product_name)
        # quantitylist.append(p.quantity)
    # print(quantitylist,'quantitylist****************')
    # print(productnames,'productnames************')

    labels =[]
    sizes = [] 
    for p in p1:
        # labels.append(p.product_name)
        labels.append(p.product_name)
        sizes.append(int(p.quantity))
    
    print(labels, 'labels')
    print(sizes,'sizes')


    
    # fig = plt.figure(figsize = (10, 5))
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels)
    
    # creating the bar plot
    # plt.bar(productnames, quantitylist, color ='maroon',
            # width = 0.4)
    
    # plt.xlabel("Product Names")
    # plt.ylabel("Quantity")
    plt.title("Quantities of different products in the warehouse")
    plt.savefig("static/graph.png")

    return '<h1> Details about the graph</h1><br><p>This graph shows remaining quantities of products in the store.</p><p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Ea consequatur quaerat, illum molestias, praesentium ipsa perferendis repellendus aperiam, deleniti vel error. Consequuntur reprehenderit facilis quos nihil nemo eos repellat, nobis illum hic, doloremque aliquam velit voluptatem porro impedit vel maxime consectetur natus rem, ipsum sit.</p><br><br><a href="static/graph.png">SHOW GRAPH</a><br><a href="/managerhomepage">Home</a>'

    























    















# ============================= run ============================
if __name__ == "__main__":
    app.run(debug=True, port=8080)
