from django.urls import path
from .views import *

urlpatterns = [
   path('',view=homePage,name="homePage"),
   path('about',view=about,name="about"),
   path('blog',view=blog,name="blog"),
   path('blogDetail',view=blogDetail,name="blogDetail"),
   path('contact',view=contact,name="contact"), 
   path('Product',view=Product,name="Product"),
   path('product-detail/',view=productDetail,name="productDetail"),
   path('shopingCart',view=shopingCart,name="shopingCart"),
   path('checkout',view=checkout,name="checkout"),
   path('login/', view=login_view, name="login"),
   path('register/',view=register_view, name="register"),
   path("profile/", view=profile_view, name="profile"),
   path('logout/', logout_view, name='logout'),
   path('forgetpassword',view=forgetpassword, name='forgetpassword'),
   path('verifyotppage',view=verifyotppage, name='verifyotppage'),
   path('resetpassword',view=resetpassword, name='resetpassword'),
   path('forgotPassword',view=forgotPassword, name='forgotPassword'),
   path('verifyOtp',view=verifyOtp, name='verifyOtp'),
   path('setNewPassword',view=setNewPassword, name='setNewPassword'),
   path('wishlistpage',view=wishlistpage,name='wishlistpage'),
   path('delivery_login',view=delivery_login,name='delivery_login'),
   path('delivery_dashboard',view=delivery_dashboard,name='delivery_dashboard'),
   path('orderpage',view=orderpage,name='orderpage'),
   path("contact/", view=contact, name="contact"),
   path("order-detail/", view=orderDetailsPage, name="orderDetailsPage"),
 
 
   
   
# USER
    path("CreateUser", view=CreateUser, name="CreateUser"),
    path("LoginUser", view=LoginUser, name="LoginUser"),
    path("verify_user_token/", view=verify_user_token, name="verify_user_token"),
    # COUNTRY
    path("countryDetail", view=countryDetail, name="countryDetail"),
    path("getAllCountry", view=getAllCountry, name="getAllCountry"),
    path("getCountryById", view=getCountryById, name="getCountryById"),
    path("CreateState", view=CreateState, name="CreateState"),
    path("getAllState", view=getAllState, name="getAllState"),
    path("getStateById", view=getStateById, name="getStateById"),
    path("CreateCity", view=CreateCity, name="CreateCity"),
    path("getAllCity", view=getAllCity, name="getAllCity"),
    path("getcityById", view=getcityById, name="getcityById"),
    path("CreatePincode", view=CreatePincode, name="CreatePincode"),
    path("getPincodeByPincode", view=getPincodeByPincode, name="getPincodeByPincode"),
    # USER PROFILE & PASSWORD
    path("createUserProfile/", view=createUserProfile, name="createUserProfile"),
    path("getUserProfile/", view=getUserProfile, name="getUserProfile"),
    path("updateUserProfile/", view=updateUserProfile, name="updateUserProfile"),
    path("deleteUserProfile/", view=deleteUserProfile, name="deleteUserProfile"),
    path("resetPassword", view=resetPassword, name="resetPassword"),
    path("forgotPassword", view=forgotPassword, name="forgotPassword"),
    path("verifyOtp", view=verifyOtp, name="verifyOtp"),
    path("setNewPassword", view=setNewPassword, name="setNewPassword"),
    # SIZE
    path("CreateSize", view=CreateSize, name="CreateSize"),
    # CATEGORIES APIS
    path("createCategory", view=createCategory, name="createCategory"),
    path("getAllCategory", view=getAllCategory, name="getAllCategory"),
    path("getSingleCategory", view=getSingleCategory, name="getSingleCategory"),
    # PRODUCT
    path("createProduct", view=createProduct, name="createProduct"),
    path("getAllProduct", view=getAllProduct, name="getAllProduct"),
    path("getSingleProduct", view=getSingleProduct, name="getSingleProduct"),
    path("productImage", view=productImage, name="productImage"),
    # CART
   #  path("createCart", view=createCart, name="createCart"),
    path("addToCart", view=addToCart, name="addToCart"),
    path("removeCartItem", view=removeCartItem, name="removeCartItem"),
    path("getAllCart", view=getAllCart, name="getAllCart"),
    path("getSingleCart", view=getSingleCart, name="getSingleCart"),
    path("removeCart", view=removeCart, name="removeCart"),
    path("cartItemQuantityPlusOrMinus",view=cartItemQuantityPlusOrMinus,name="cartItemQuantityPlusOrMinus"),
    path("addAddress", view=addAddress, name="addAddress"),
    path("getAllAddressesOfUser",view=getAllAddressesOfUser,name="getAllAddressesOfUser"),
    path("updateOrderAddress",view=updateOrderAddress,name="updateOrderAddress"),
    path("getSingleAddress", view=getSingleAddress, name="getSingleAddress"),
    path("updateAddress", view=updateAddress, name="updateAddress"),
    path("removeAddress", view=removeAddress, name="removeAddress "),
    # ORDER
    path("createOrder/", view=createOrder, name="createOrder"),
    path("getCurrentOrder", view=getCurrentOrder, name="getCurrentOrder"),
    path("getOrderHistory", view=getOrderHistory, name="getOrderHistory"),
    path("getOrderHistoryById/", view=getOrderHistoryById, name="getOrderHistoryById"),
    # REVIEW
    path("CreateReviewWithImage",view=CreateReviewWithImage,name="CreateReviewWithImage"),
    path("getReviewByProductId", view=getReviewByProductId, name="getReviewByProductId"),
    path("GetReview", view=GetReview, name="GetReview"),
    
    # wishlist and banner
    path("addOrRemoveWishlist", view=addOrRemoveWishlist, name="addOrRemoveWishlist"),
    path("getWishlistByUserId", view=getWishlistByUserId, name="getWishlistByUserId"),
    path("CreateBannerImage", view=CreateBannerImage, name="CreateBannerImage"),
    path("getAllBanners", view=getAllBanners, name="getAllBanners"),
    path("chatbot", view=chatbot, name="chatbot"),
    path("clearChatSession", view=clearChatSession, name="clearChatSession"),

   #  stock
    path("createStock", view=createStock, name="createStock"),
    path("getProductStock", view=getProductStock, name="getProductStock"),

   #  DELIVERY
    path("deliveryLogin", view=deliveryLogin, name="deliveryLogin"),
    path("deliveryDashboard", view=deliveryDashboard, name="deliveryDashboard"),
    path("getUnassignedOrders", view=getUnassignedOrders, name="getUnassignedOrders"),
    path("getSingleOrder/<int:order_id>/", view=getSingleOrder, name="getSingleOrder"),
    path("acceptDeliveryOrder", view=acceptDeliveryOrder, name="acceptDeliveryOrder"),
    path("markOutForDelivery", view=markOutForDelivery, name="markOutForDelivery"),
    path("completeDelivery", view=completeDelivery, name="completeDelivery"),
    path("updateDeliveryProfile", view=updateDeliveryProfile, name="updateDeliveryProfile"),
    path("accept/<int:order_id>/", view=acceptPage, name="acceptPage"),
    path("delivery_order_detail/<int:order_id>/", view=deliveryOrderDetail, name="deliveryOrderDetail"),

]



   # # USER REGISTER - API
   #  path('CreateUser',view=CreateUser,name="CreateUser"),
   #  path("verify-token/", view=verify_user_token, name="verify_token"),
   #  path("verify_user_token", verify_user_token, name="verify_user_token"),


   # path('getUserProfile',view=getUserProfile,name="getUserProfile"),
   # path('updateUserProfile',view=updateUserProfile,name="updateUserProfile"),
   # path('deleteUserProfile',view=deleteUserProfile,name="deleteUserProfile"),

   # # LOGIN USER
   # path('LoginUser',view=LoginUser,name="LoginUser"),
   # #country -api
   # path('countryDetail',view=countryDetail,name="countryDetail"),
   # #GETALLCOUNTRY API
   # path('getAllCountry',view=getAllCountry,name="getAllCountry"),
   # #COUTRYBYID API
   # path('getCountryById',view=getCountryById,name="getCountryById"),
   # #state-api
   # path('CreateState',view=CreateState,name="CreateState"),
   # #GETALLSTATE API
   # path('getAllState',view=getAllState,name="getAllState"),
   # #STATEBY ID -API
   # path('getStateById',view=getStateById,name="getStateById"),

   # #city-api
   # path('CreateCity',view=CreateCity,name="CreateCity"),
   # #PINCODE API
   # path('CreatePincode',view=CreatePincode,name="CreatePincode"),
   # #LOGINUSER API
   # # path('LoginUser',view=LoginUser,name="LoginUser"),
   # #PROFILE API
   # path('createUserProfile',view=createUserProfile,name="createUserProfile"),
   # #SIZE API
   # path('CreateSize',view=CreateSize,name="CreateSize"),
   # #CATEGORY API 
   # path('createCategory',view=createCategory,name="createCategory"),
   # #GETALL CATEGORY API
   # path('getAllCategory',view=getAllCategory,name="getAllCategory"),
   # #GETCATEGORYBY -ID API
   # path('getSingleCategory',view=getSingleCategory,name="getSingleCategory"),
   # #PRODUCT API
   # path('createProduct',view=createProduct,name="createProduct"),
   # #GETALLPRODUCT API
   # path('getAllProduct',view=getAllProduct,name="getAllProduct"),
   # #PRODUCTIMAGE API 
   # path('productImage',view=productImage,name="productImage"),
   # #GETPRODUCTIMAGE API 
   # path('getSingleProduct',view=getSingleProduct,name="getSingleProduct"),
   # #ADDRESS API 
   # path('createAdress',view=createAdress,name="createAdress"),

   # #wishlist
   # path('getWishlistByUserId',view=getWishlistByUserId,name="getWishlistByUserId"),
   # path('addOrRemoveWishlist',view=addOrRemoveWishlist,name="addOrRemoveWishlist"),
   # #CART-ITEM API
   # path('addToCart',view=addToCart,name="addToCart"),
   # path('removeCartItem',view=removeCartItem,name="addToCart"),
   # path('getAllCart',view=getAllCart,name="getAllCart"),
   # path('getSingleCart',view=getSingleCart,name="getSingleCart"),
   # path('removeCart',view=removeCart,name="removeCart"),
   # path('cartItemQuantityPlusOrMinus',view=cartItemQuantityPlusOrMinus,name="cartItemQuantityPlusOrMinus"),
   # #ORDER API
   # path('createOrder',view=createOrder,name="createOrder"),
   
   # #BANNERIMAGE API
   # path('CreateBannerImage',view=CreateBannerImage,name="CreateBannerImage")


