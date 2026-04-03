from django.contrib import admin
from django.contrib.auth.hashers import make_password

# Register your models here

from .models import *


class countryAdmin(admin.ModelAdmin):
    list_display = ["country_id", "country_name", "country_code", "dial_code"]


admin.site.register(country, countryAdmin)


class stateAdmin(admin.ModelAdmin):
    list_display = ["state_id", "state_name", "country_id"]


admin.site.register(state, stateAdmin)


class cityAdmin(admin.ModelAdmin):
    list_display = ["city_id", "city_name", "state_id"]


admin.site.register(city, cityAdmin)


class pincodeAdmin(admin.ModelAdmin):
    list_display = ["pincode_id", "pincode", "city_id"]


admin.site.register(pincode, pincodeAdmin)


class userAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
        "username",
        "country_code",
        "phone_number",
        "email",
        "password",
        "otp",
        "created_at",
        "updated_at",
    ]


admin.site.register(user, userAdmin)


class profileAdmin(admin.ModelAdmin):
    list_display = [
        "profile_id",
        "first_name",
        "last_name",
        "gender",
        "DOB",
        "profile_picture",
        "is_active",
        "is_deleted",
        "user_id",
    ]


admin.site.register(profile, profileAdmin)


class sizeAdmin(admin.ModelAdmin):
    list_display = ["size_id", "size_name", "parent_size"]


admin.site.register(size, sizeAdmin)


class categoryAdmin(admin.ModelAdmin):
    list_display = ["category_id", "category_name", "parent_category"]


admin.site.register(category, categoryAdmin)


class productAdmin(admin.ModelAdmin):
    list_display = ["product_id", "product_name", "category"]


admin.site.register(product, productAdmin)


class productImagesAdmin(admin.ModelAdmin):
    list_display = ["image_id", "images", "product_id", "color"]


admin.site.register(productImages, productImagesAdmin)


class addressAdmin(admin.ModelAdmin):
    list_display = ["address_id", "street_address", "user_id", "full_name"]


admin.site.register(address, addressAdmin)


class tokensAdmin(admin.ModelAdmin):
    list_display = ["token_id", "user_id", "tokens"]


admin.site.register(tokens, tokensAdmin)


class cartAdmin(admin.ModelAdmin):
    list_display = ["cart_id", "user_id", "grand_total", "is_active"]


admin.site.register(cart, cartAdmin)


class cartItemsAdmin(admin.ModelAdmin):
    list_display = [
        "cart_item_id",
        "cart_id",
        "product_id",
        "size",
        "price",
        "quantity",
        "color",
    ]


admin.site.register(cartItems, cartItemsAdmin)


class orderAdmin(admin.ModelAdmin):
    list_display = [
        "order_id",
        "cart_id",
        "user_id",
        "grand_total",
        "status",
        "address_id",
    ]


admin.site.register(order, orderAdmin)


class orderItemsAdmin(admin.ModelAdmin):
    list_display = [
        "order_item_id",
        "product_id",
        "order_id",
        "quantity",
        "price",
        "size",
    ]


admin.site.register(orderItems, orderItemsAdmin)


class reviewAdmin(admin.ModelAdmin):
    list_display = [
        "review_id",
        "product_id",
        "order_item_id",
        "user_id",
        "rating",
        "comment",
    ]


admin.site.register(review, reviewAdmin)


class reviewImageAdmin(admin.ModelAdmin):
    list_display = ["review_image_id", "image", "review_id"]


admin.site.register(reviewImage, reviewImageAdmin)


class wishlistAdmin(admin.ModelAdmin):
    list_display = ["wishlist_id", "user_id", "product_id"]


admin.site.register(wishlist, wishlistAdmin)


class bannerImagesAdmin(admin.ModelAdmin):
    list_display = ["banner_id", "image"]


admin.site.register(bannerIamges, bannerImagesAdmin)


class stockAdmin(admin.ModelAdmin):
    list_display = ("stock_id", "product_id", "stock_quantity", "size_id")


admin.site.register(stock, stockAdmin)


class cardDetailAdmin(admin.ModelAdmin):
    list_display = (
        "card_id",
        "card_holder_name",
        "card_number",
        "card_cvv",
        "card_expiry",
        "card_balance",
    )


admin.site.register(cardDetail, cardDetailAdmin)


class deliveryPersonAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.password and not obj.password.startswith("pbkdf2_"):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

    list_display = (
        "delivery_person_id",
        "password",
        "delivery_person_name",
        "mobile",
        "email",
        "wallet",
    )


admin.site.register(deliveryPerson, deliveryPersonAdmin)


class deliveryTokensAdmin(admin.ModelAdmin):
    list_display = ("token_id", "delivery_person_id", "tokens", "exp_time")


admin.site.register(deliveryTokens, deliveryTokensAdmin)


class orderHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "user_id",
        "address_id",
        "delivery_person_id",
        "message",
        "created_at",
    )


admin.site.register(orderHistory, orderHistoryAdmin)


class additionalInformationAdmin(admin.ModelAdmin):
    list_display = ("additional_information_id", "product_id", "label", "label_data")


admin.site.register(additionalInformation, additionalInformationAdmin)


class colorAdmin(admin.ModelAdmin):
    list_display = ("color_id", "color_name", "color_code")


admin.site.register(color, colorAdmin)
