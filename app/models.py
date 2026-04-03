from django.db import models
import uuid
 
# Create your models here.
class country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=200)
    country_code = models.CharField()
    dial_code = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.country_name)
 
class state(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=200)
    country_id = models.ForeignKey(country,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.state_name)
 
class city(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=200)
    state_id = models.ForeignKey(state, on_delete =models.CASCADE,null = True,blank=True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.city_name)
   
class pincode(models.Model):
    pincode_id = models.AutoField(primary_key=True)
    pincode = models.IntegerField()
    city_id = models.ForeignKey(city,on_delete=models.CASCADE,null = True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.pincode)
 
class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    country_code = models.ForeignKey(country,on_delete=models.CASCADE,null=True,blank=True)
    phone_number = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=150)
    otp = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.user_id)
   
class profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender_Choice=(
        (0,'Female'),
        (1,'Male'),
        (2,'Other'),
    )
    gender=models.IntegerField(choices=gender_Choice,default=0,null=True)
    DOB = models.DateField()
    profile_picture = models.ImageField(upload_to="profile")
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.first_name)
 
class size(models.Model):
    size_id = models.AutoField(primary_key=True)
    size_name = models.CharField(max_length=200)
    parent_size = models.ForeignKey("self",on_delete=models.CASCADE,null = True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.size_name)
 
class category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    parent_category = models.ForeignKey("self",on_delete=models.CASCADE,null = True,blank=True)
    category_image = models.ImageField(upload_to="media/category")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.category_name)
    
class color(models.Model):
    color_id = models.AutoField(primary_key=True)
    color_name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7)

    def __str__(self):
        return str(self.color_name)
   
class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(category,on_delete=models.CASCADE,null=True,blank=True)
    size = models.ManyToManyField(size,related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    color = models.ManyToManyField(color, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.product_name)
   
class productImages(models.Model):
    image_id = models.AutoField(primary_key=True)
    images = models.FileField(upload_to="product")
    product_id = models.ForeignKey(product,on_delete=models.CASCADE,blank = True,null=True)
    color = models.ForeignKey(color,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.images)
   
class address(models.Model):
    address_id = models.AutoField(primary_key=True)
    street_address =models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    pincode = models.ForeignKey(pincode,on_delete=models.CASCADE,blank = True,null=True)
    user_id = models.ForeignKey(user,on_delete=models.CASCADE,blank = True,null=True)
    is_active = models.BooleanField(default=True)
    full_name = models.CharField(max_length=200)
    dial_code = models.CharField(max_length=4)
    phone_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.address_id)
   
class tokens(models.Model):
    token_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user,on_delete=models.CASCADE,blank=True,null=True)
    tokens = models.CharField(max_length=255)
    exp_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.token_id)
   
class cart(models.Model):
    cart_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(user,on_delete=models.SET_NULL,null=True,blank=True)
    grand_total=models.DecimalField(decimal_places=2, max_digits=10)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.cart_id)
   
class cartItems(models.Model):
    cart_item_id=models.AutoField(primary_key=True)
    cart_id=models.ForeignKey(cart,on_delete=models.SET_NULL,null=True,blank=True)
    product_id=models.ForeignKey(product,on_delete=models.SET_NULL,null=True,blank=True)
    size=models.ForeignKey(size,on_delete=models.SET_NULL,null=True,blank=True)
    price=models.DecimalField(decimal_places=2, max_digits=10)
    total = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    quantity=models.IntegerField()
    color = models.ForeignKey(color,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.quantity)

class deliveryPerson(models.Model):
    delivery_person_id = models.AutoField(primary_key=True)
    delivery_person_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255,null=True)
    mobile = models.IntegerField()
    email = models.EmailField()
    city = models.ForeignKey(city,on_delete=models.CASCADE,null=True,blank=True)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.delivery_person_name)

class deliveryTokens(models.Model):
    token_id = models.AutoField(primary_key=True)
    delivery_person_id = models.ForeignKey(deliveryPerson,on_delete=models.CASCADE,blank=True,null=True)
    tokens = models.CharField(max_length=255)
    exp_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.token_id)

class order(models.Model):
    order_id=models.AutoField(primary_key=True)
    serial_no = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )
    cart_id=models.ForeignKey(cart,on_delete=models.SET_NULL,null=True,blank=True)
    user_id=models.ForeignKey(user,on_delete=models.SET_NULL,null=True,blank=True)
    grand_total=models.DecimalField(decimal_places=2, max_digits=10)
    status_Choice=(          
    (0, 'Confirmed'),            
    (1, 'Assigned'),            
    (2, 'Accepted'),            
    (3, 'Out for Delivery'),    
    (4, 'Delivered'),            
    (5, 'Cancelled'),            
    (6, 'Failed'),              
    (7, 'Returned'),
    (8, 'Parcel Through')            
)
    status=models.IntegerField(choices=status_Choice,default=0,null=True)
    address_id=models.ForeignKey(address,on_delete=models.SET_NULL,null=True,blank=True)
    paymentChoices = (
        (0,'Cash'),
        (1,'Card')
    )
    payment_choices = models.IntegerField(choices=paymentChoices,default=0, null=True)
    paymentStatus = (
        (0,'Pending'),
        (1,'Captured')
    )
    payment_status = models.IntegerField(choices=paymentStatus,default=0, null=True)
    delivery_charges = models.DecimalField(max_digits=19,decimal_places=2, null=True)
    assigned_delivery_person = models.ForeignKey(deliveryPerson,on_delete=models.SET_NULL,null=True,blank=True,related_name="assigned_orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.serial_no:
            self.serial_no = "ORD" + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.order_id)
 
  
class orderItems(models.Model):
    order_item_id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(product,on_delete=models.CASCADE,null=True,blank=True)
    order_id=models.ForeignKey(order,on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField()
    price=models.DecimalField(decimal_places=2, max_digits=10)
    size=models.ForeignKey(size,on_delete=models.SET_NULL,null=True,blank=True)
    color = models.ForeignKey(color, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.price)
   
class review(models.Model):
    review_id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(product,on_delete=models.CASCADE,null=True,blank=True)
    order_item_id=models.ForeignKey(order,on_delete=models.CASCADE,null=True,blank=True)
    user_id=models.ForeignKey(user,on_delete=models.CASCADE,null=True,blank=True)
    rating=models.IntegerField()
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.comment)
   
class reviewImage(models.Model):
    review_image_id=models.AutoField(primary_key=True)
    image=models.FileField(upload_to="review")
    review_id=models.ForeignKey(review,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.image)
   
class wishlist(models.Model):
    wishlist_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(user,on_delete=models.CASCADE,null=True,blank=True)
    product_id=models.ForeignKey(product,on_delete=models.CASCADE,null=True,blank=True)
    color = models.ForeignKey(color, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return str(self.wishlist_id)
   
class bannerIamges(models.Model):
    banner_id=models.AutoField(primary_key=True)
    image=models.FileField(upload_to="media/banner")
 
    def __str__(self):
        return str(self.image)
 
class stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(product,on_delete=models.CASCADE,null=True,blank=True)
    stock_quantity = models.IntegerField()
    color_id = models.ForeignKey(color,on_delete=models.CASCADE,null=True,blank=True)
    size_id = models.ForeignKey(size,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.stock_id)

class cardDetail(models.Model):
    card_id = models.AutoField(primary_key=True)
    card_holder_name = models.CharField(max_length=255)
    card_number = models.BigIntegerField()
    card_cvv = models.IntegerField()
    card_expiry = models.IntegerField()
    card_balance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return str(self.card_holder_name)
    
class orderHistory(models.Model):
    order_history_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(order, on_delete=models.CASCADE)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    address_id = models.ForeignKey(address, on_delete=models.CASCADE)
    delivery_person_id = models.ForeignKey(deliveryPerson,on_delete=models.SET_NULL,null=True,blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order_history_id)
    
class additionalInformation(models.Model):
    additional_information_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=255)
    label_data = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.label)