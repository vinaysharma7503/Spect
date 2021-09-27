from flask import Flask, render_template,request, make_response,session,redirect
from mailer import mailer
import re
from elastics import retrieve
import json

app = Flask(__name__)
app.secret_key = 'super secret key'
ip = "www.spectevo.in"

# Make a regular expression 
# for validating an Email 
regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

@app.route('/',methods=['GET','POST'])
def index_start(msg = ""):
	if len(msg) > 0:
		return render_template("/index.html",popup = 1,msg=msg)
	else:
		return render_template("/index.html",popup = 0)

@app.route("/turnkey",methods=['GET','POST'])
def turnkeyindex():
	page = request.args.get("page")
	pagename = "/turnkey/{}.html".format(page)
	return render_template(pagename)

@app.route("/lab",methods=['GET','POST'])
def labindex():
	page = request.args.get("page")
	pagename = "/lab/{}.html".format(page)
	return render_template(pagename)

@app.route('/contactus',methods=['GET','POST'])
def contactus():
	name = request.form.get("name")
	email = request.form.get("email")
	phone = request.form.get("phone")
	subject = request.form.get("subject")
	message = request.form.get("message")
	page = request.form.get("page","")
	subjectMain = email+"-Website query"
	html = "Name :{}<br>Email :{}<br>Phone :{}<br>Subject :{}<br>Message :{}<br>".format(name,email,phone,subject,message)
	cEmail = check_email(email)
	if cEmail == 0:
		if page == "getlist":
			return itemlist("Please provide a proper Email Id")
		else:
			return index_start("Please provide a proper Email Id")

	# mailer(html, email,subjectMain)
	mailer(html, "info@spectevo.com",subjectMain)
	if page == "getlist":
		return itemlist("Email Sent successfully")
	else:
		return index_start("Email Sent successfully")


@app.route("/getlist",methods=['GET','POST'])
def itemlist(msgI =""):
	character = request.args.get("char","A")
	f = request.args.get("page",0)
	character = character if character != "None" else "A"
	f = f if f != "None" else 0
	session["previouslink"] = "/getlist?char={}&page={}".format(character,f)
	f = int(f)*10
	pageno = str(int(request.args.get("page","0")) + 1)
	print (f)
	size = 10
	body = {}
	body["from"] = f
	body["size"] = 10
	body["query"] = {"match":{"char":character}}
	data = retrieve(body)
	listD = data.get("hits").get("hits")
	newlistD = []
	for d in listD:
		newlistD.append(d.get("_source"))
	listofalpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	pagenumber = int(request.args.get("page",0))
	pages = []
	print (pagenumber)
	if pagenumber % 5 == 0:
		for i in range(pagenumber,pagenumber+5):
			pages.append(str(i+1))
		session["pages"] = pages

	pages = session.get("pages")
	msg = request.args.get("msg","")
	if len(msg) == 0:
		popup = 0
	else:
		popup=1


	cart = session.get("cart",[])
	total = 0
	for c in cart:
		quantity = int(c.get("quantity"))
		price = float(c.get("price"))
		total += price*quantity

	total = round(total,2)
	if len(msgI) > 0:
		msg = msgI
		popup = 1

	return render_template("/faqs.html",data=newlistD,listofalpha=listofalpha,pages=pages,pageno = pageno,char=character,popup=popup,msg=msg,cart=cart,lencart=len(cart),total=total)

@app.route("/addtocart",methods=['GET','POST'])
def addtocard():
	print (request.args)
	pack = request.args.get("pack")
	price=request.args.get("price")
	name = request.args.get("name")
	cas = request.args.get("cas")
	cno = request.args.get("cno")
	char = request.args.get("char")
	page = request.args.get("page")
	gst = request.args.get("gst","18%")
	hsn = request.args.get("hsn","2942")
	quantity = request.args.get("quantity","1")
	if len(hsn) == 0:
		hsn = "2942"
		gst = "18%"
	hsn = hsn[0]+hsn[1]+hsn[2]+hsn[3]
	cart = session.get("cart",[])
	print (cart,"cart")
	previouslink = session.get("previouslink")
	for d in cart:
		packT = d.get("pack")
		cnoT = d.get("cno")
		print (pack,packT)
		if (pack == packT) and (cnoT == cno):
			msg = "Product already exists"
			return redirect(previouslink)
	jsonD = {}
	jsonD["pack"] = pack
	jsonD["price"] = price
	jsonD["name"] = name
	jsonD["cas"] = cas
	jsonD["cno"] = cno
	jsonD["gst"] = gst
	jsonD["hsn"] = hsn
	jsonD["quantity"] = quantity
	jsonD["amount"] = str(round(float(jsonD.get("price")) * int(jsonD.get("quantity")),2))
	cart.append(jsonD)
	session["cart"] = cart
	msg = "Item added to cart"
	return make_response(json.dumps({"url":previouslink}))


@app.route("/checkout",methods=['GET','POST'])
def checkout():
	cart = session.get("cart",[])
	session["previouslink"] = "/checkout"
	total = 0
	gsttotal = 0
	for c in cart:
		quantity = int(c.get("quantity"))
		price = float(c.get("price")) * quantity
		gst = c.get("gst")
		gst = float(gst.split("%")[0])
		gstT = (price*gst)/100
		gsttotal += gstT
		total += price
	total = round(total,2)
	gsttotal = round(gsttotal,2)
	gtotal = gsttotal + total
	gtotal = round(gtotal,2)
	return render_template("/cart.html",cart=cart,lencart = len(cart),total=total,gsttotal=gsttotal,gtotal=gtotal)

@app.route("/remove",methods=['GET','POST'])
def remove():
	cart = session.get("cart",[])
	cas = request.args.get("cas")
	pack = request.args.get("pack")
	newcart = []
	for d in cart:
		packT = d.get("pack")
		casT = d.get("cas")
		print (pack,packT)
		print (casT,cas)
		if (pack == packT) and (casT == cas):
			print ("went in")
			continue
		else:
			newcart.append(d)
	session["cart"] = newcart
	previouslink = session.get("previouslink")
	return redirect(previouslink)

def check_email(email):  

    if(re.search(regex,email)):  
        return 1
          
    else:  
        return 0

@app.route("/search",methods=['GET','POST'])
def search():
	search = request.args.get("search","").lower()
	body = {}
	body["query"] = {"match":{"tags":search}}
	data = retrieve(body)
	listD = data.get("hits").get("hits")
	finalD = []
	for data in listD:
		jsonD = data.get("_source")
		finalD.append(jsonD)
	cart = session.get("cart",[])
	total = 0
	for c in cart:
		quantity = int(c.get("quantity"))
		price = float(c.get("price")) * quantity
		total += price

	total = round(total,2)
	listofalpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	session["previouslink"] = "/search?search={}".format(search)
	return render_template("/faqs.html",data=finalD,listofalpha=listofalpha,pages=["0"],pageno = "0",char="",popup=0,msg="",cart=cart,lencart=len(cart),total=total,search="true")

@app.route("/submit",methods=['GET','POST'])
def submit():
	print (request.form)
	name = request.form.get("name")
	cname = request.form.get("cname")
	mob = request.form.get("mob")
	email = request.form.get("email")
	gstreduce = request.form.get("gstreduce","")
	print (gstreduce,"gst")
	cart = session.get("cart",[])
	session["previouslink"] = "/checkout"
	total = 0
	gsttotal = 0
	newlist = []
	for c in cart:
		quantity = int(c.get("quantity"))
		price = float(c.get("price")) * quantity
		if gstreduce == "true":
			c["gst"] = '5%'
			gst = "5%"
		else:
			gst = c.get("gst")
		gst = float(gst.split("%")[0])
		gstT = (price*gst)/100
		gsttotal += gstT
		total += price
		newlist.append(c)
	total = round(total,2)
	gsttotal = round(gsttotal,2)
	gtotal = gsttotal + total
	gtotal = round(gtotal,2)

	if gstreduce == "true":
		gsttotal = round(total * 0.05,2)
		gtotal = round(total + gsttotal,2)

	flag = check_email(email)
	if len(name) < 3:
		return render_template("/cart.html",gstreduce=gstreduce,cart=cart,lencart = len(cart),total=total,gsttotal=gsttotal,gtotal=gtotal,popup=1,msg="Please provide a proper name",name=name,cname=cname,mob=mob,email=email)
	if len(cname) <1:
		return render_template("/cart.html",gstreduce=gstreduce,cart=cart,lencart = len(cart),total=total,gsttotal=gsttotal,gtotal=gtotal,popup=1,msg="Please provide a proper company name",name=name,cname=cname,mob=mob,email=email)
	if len(mob) < 10:
		return render_template("/cart.html",gstreduce=gstreduce,cart=cart,lencart = len(cart),total=total,gsttotal=gsttotal,gtotal=gtotal,popup=1,msg="Please provide a proper mobile number",name=name,cname=cname,mob=mob,email=email)
	if flag == 0:
		return render_template("/cart.html",gstreduce=gstreduce,cart=cart,lencart = len(cart),total=total,gsttotal=gsttotal,gtotal=gtotal,popup=1,msg="Please provide a proper email",name=name,cname=cname,mob=mob,email=email)

	html = render_template("/template.html",gstreduce=gstreduce,cart=newlist,lencart = len(cart),total=total,gsttotal=gsttotal,gtotal=gtotal,name=name,cname=cname,mob=mob,email=email)
	mailer(html, email,"Product enquiry")
	print("sending to info")
	mailer(html, "info@spectevo.com", "Product enquiry")
	print ("sent")
	session["cart"] = []
	return redirect("/getlist?msg={}".format("Thank you for your query we will contact you shortly"))


if __name__ == '__main__':
    app.run(debug="true",port=5000,host='0.0.0.0')