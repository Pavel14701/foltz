from products.models import ProductSection, Product, ProductCategory, ProductSubCategory, ProductTags
from graphql import GraphQLError
from site_api.schema_product.inputs import ProductSectionInput, ProductInput, ProductSubCategoryInput


def find_product(_input:ProductSectionInput|ProductInput) -> Product:
    product = None
    if _input.product_pk:
        try:
            product = Product.objects.get(pk=_input.product_pk)
        except Product.DoesNotExist as e:
            raise GraphQLError("Product not found by pk.") from e
    elif _input.product_title:
        try:
            product = Product.objects.get(title=_input.product_title)
        except Product.DoesNotExist as e:
            raise GraphQLError("Product not found by title.") from e
    else:
        raise GraphQLError("Either product_pk or product_title must be provided.")
    return product


def find_product_section(_input:ProductSectionInput) -> ProductSection:
    product = find_product(_input)
    try:
        product_section = ProductSection.objects.get(product=product, order=_input.old_order)
    except ProductSection.DoesNotExist as e:
        raise GraphQLError("Product section not found.")  from e
    return product_section


def validate_section_input(_input:ProductSectionInput) -> ProductSectionInput:
    filled_fields = [
        _input.subtitle, _input.content,
        _input.content, _input.youtube_url, 
        _input.image, _input.add,
        _input.characteristics
    ]
    non_empty_fields = [field for field in filled_fields if field is not None]
    if len(non_empty_fields) != 1:
        raise ValueError('Only one of subtitle, content, youtube_url, or image must be filled.')
    return _input


def null_section(product_section:ProductSection) -> ProductSection:
    product_section.subtitle = None
    product_section.content = None
    product_section.youtube_url = None
    product_section.image = None
    product_section.add = None
    product_section.characteristics = None
    return product_section

def save_section(_input:ProductSectionInput, section:ProductSection=None, product:Product=None) -> ProductSection:
    if product:
        section = ProductSection(
            product=product,
            order=_input.new_order,
            subtitle=_input.subtitle,
            content=_input.content,
            youtube_url=_input.youtube_url,
            image=_input.image,
            add=_input.add,
            characteristics=_input.characteristics
        )
        section.save()
        return section
    if _input.new_order is not None:
        section.order = _input.order
    if _input.subtitle is not None:
        section.subtitle = _input.subtitle
    if _input.content is not None:
        section.content = _input.content
    if _input.youtube_url is not None:
        section.youtube_url = _input.youtube_url
    if _input.image is not None:
        section.image = _input.image
    if _input.add is not None:
        section.add = _input.add
    if _input.characteristics is not None:
        section.characteristics = _input.characteristics
    section.save()
    return section


def save_product(_input:ProductInput, product:Product=None, category:ProductCategory=None,\
    subcategory:ProductSubCategory=None) -> Product:
    if product is None:
        product = Product(
            title=_input.new_product_title,
            preview_text=_input.preview_text,
            preview_video_url=_input.preview_video_url,
            preview_image=_input.preview_image,
            category=category,
            subcategory=subcategory,
            price=_input.price,
            quantity=_input.quantity
        )
        product.save()
        return product
    if title:=_input.new_product_title is not None:
        product.title = title
    if preview_text:=_input.preview_text is not None:
        product.preview_text = preview_text
    if preview_video_url:=_input.preview_video_url is not None:
        product.preview_image = None
        product.preview_video_url = preview_video_url
    if preview_image:=_input.preview_image is not None:
        product.preview_video_url = None
        product.preview_image = preview_image
    if category:=_input.category is not None:
        product.category = category
    if subcategory:=_input.subcategory is not None:
        product.subcategory = subcategory
    if price:=_input.price is not None:
        product.price = price
    if quantity:=_input.quantity is not None:
        product.quantity=quantity
    product.save()
    return product


def validate_input_cat_subcat(_input:ProductInput, flag:bool=None) -> tuple[ProductCategory, ProductSubCategory]:
    if flag is None:
        if not _input.category:
            raise GraphQLError("Category must be provided.")
        if not _input.subcategory:
            raise GraphQLError("Subcategory must be provided.")
    try:
        if _input.category is None:
            category = None
        else:
            category = ProductCategory.objects.get(name=_input.category)
    except ProductCategory.DoesNotExist as e:
        raise GraphQLError("Category not found.") from e
    try:
        if _input.subcategory is None:
            subcategory = None
        else:
            subcategory = ProductSubCategory.objects.get(name=_input.subcategory)
    except ProductSubCategory.DoesNotExist as e:
        raise GraphQLError("Subcategory not found.") from e
    return category, subcategory


def add_tags(_input:ProductInput, product:Product) -> Product:
    if _input.tags:
        for tag_name in _input.tags:
            tag, created = ProductTags.objects.get_or_create(name=tag_name)
            product.tags.add(tag)
    product.save()
    return product


def remove_tags(_input: ProductInput, product: Product) -> Product:
    if _input.tags_to_del:
        for tag_name in _input.tags_to_del:
            try:
                tag = ProductTags.objects.get(name=tag_name)
                product.tags.remove(tag)
            except ProductTags.DoesNotExist:
                continue
    product.save()
    return product

def get_category(_input:ProductSubCategoryInput) -> ProductCategory:
    if _input.category_pk:
        try:
            return ProductCategory.objects.get(pk=_input.category_pk)
        except ProductCategory.DoesNotExist as e:
            raise GraphQLError("Category not found by ID.") from e
    elif _input.category_name:
        try:
            return ProductCategory.objects.get(name=_input.category_name)
        except ProductCategory.DoesNotExist as e:
            raise GraphQLError("Category not found by name.") from e
    else:
        raise GraphQLError(
            "Either category ID or category \
            name must be provided."
        )


def get_subcategory(_input:ProductSubCategoryInput) -> ProductSubCategory:
    category = get_category(_input)
    try:
        if _input.pk:
            return ProductSubCategory.objects.get(pk=_input.pk, category=category)
    except ProductSubCategory.DoesNotExist as e:
        raise GraphQLError("SubCategory not found in the specified category") from e