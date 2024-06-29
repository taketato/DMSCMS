
from create_database import app, db, User, Product, Inventory, Delivery, Items, contract_ABI


def add_user(name, type, email, password, token, sc_address):
    with app.app_context():
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is None:
            new_user = User(name=name, type=type, email=email, password=password, token=token, sc_address=sc_address)
            db.session.add(new_user)
            db.session.commit()
        else:
            print(f"User with id {id} already exists.")


def delete_user(email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            print(f"No user found with email: {email}")


def update_user(name, new_type=None, new_email=None):
    with app.app_context():
        user = User.query.filter_by(name=name).first()
        if user:
            if new_type:
                user.type = new_type
            if new_email:
                user.email = new_email
            db.session.commit()
        else:
            print(f"No user found with id: {id}")


# update
def query_user_name(name):
    with app.app_context():
        user = User.query.filter_by(name=name).first()
        if user:
            return user.id, user.type, user.email, user.sc_address
        else:
            print(f"No user found with name: {name}")
            return None

def query_user_id(id):
    with app.app_context():
        user = User.query.filter_by(id=id).first()
        if user:
            return user.name, user.type, user.email, user.sc_address
        else:
            print(f"No user found with id: {id}")
            return None

def query_user_name_type(name, type):
    with app.app_context():
        user = User.query.filter_by(name=name, type=type).first()
        if user:
            return user.id, user.email, user.token, user.sc_address
        else:
            print(f"No user found with name: {name}")
            return None


def query_token_with_email(email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            return user.token, user.name, user.type, user.id, user.sc_address
        else:
            print(f"No user found with email: {email}")
            return None
        

def update_user_token(new_token=None, email=None):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            if new_token:
                user.token = new_token
                # user.token = None
            db.session.commit()
        else:
            print(f"No user found with id: {id}")
            
            
def delete_token(token):
    with app.app_context():
        user = User.query.filter_by(token=token).first()
        if user:
            user.token = None
            db.session.commit()
        else:
            print(f"No user found with token")


# update
def query_user_email(email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            return user.type, user.password, user.sc_address, user.name, user.email
        else:
            print(f"No user found with email: {email}")
            return None


def add_product(user_id, name, type):
    with app.app_context():
        # existing_product = Product.query.filter_by(id=id).first()
        # if existing_product is None:
        new_product = Product(name=name, type=type, user_id=user_id)
        db.session.add(new_product)
        db.session.commit()
        # else:
        #     print(f"Product with id {id} already exists.")


# update
def delete_product(name):
    with app.app_context():
        product = Product.query.filter_by(name=name).first()
        if product:
            db.session.delete(product)
            db.session.commit()
        else:
            print(f"No product found")


# update
def update_product(name, new_type=None):
    with app.app_context():
        product = Product.query.filter_by(name=name).first()
        if product:
            if new_type:
                product.type = new_type
            db.session.commit()
        else:
            print(f"No product found")

# update
def query_product(name):
    with app.app_context():
        product = Product.query.filter_by(name=name).first()
        if product:
            return product.id
        else:
            print(f"No product found")
            return None

def query_product_id(id):
    with app.app_context():
        product = Product.query.filter_by(id=id).first()
        if product:
            return product.type, product.name, product.user_id
        else:
            print(f"No product found")
            return None

# def query_product_patient():
#     with app.app_context():
#         product = Product.query.filter_by(id=id).first()
#         if product:
#             return product.type, product.name, product.user_id
#         else:
#             print(f"No product found")
#             return None

# # update
# def query_product_id(user_id):
#     with app.app_context():
#         product = Product.query.filter_by(user_id=user_id).first()
#         if product:
#             return product.name
#         else:
#             print(f"No product found with")
#             return None


def query_product_user_id(email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            ItemNames = Product.query.filter(Product.user_id == user.id).all()
            # for ItemName in ItemNames:
            #     print(ItemName.name)
            ItemName = [ItemName.name for ItemName in ItemNames]
            # if ItemNames:
            return ItemName


# add name
def add_inventory(user_id, pid, name, inventory_quantity, demand_quantity):
    with app.app_context():
        existing_production = Inventory.query.filter_by(user_id=user_id, name=name, pid=pid).first()
        if not existing_production:
            new_production = Inventory(name=name, pid=pid, InventoryQuantity=inventory_quantity, DemandQuantity=demand_quantity, user_id=user_id)
            db.session.add(new_production)
            db.session.commit()
        else:
            return None
        # else:
        #     print(f"Production with id {id} already exists.")


# update
def delete_inventory_production(delete_id, name):
    with app.app_context():
        production = Inventory.query.filter_by(user_id=delete_id, name=name).first()
        if production:
            db.session.delete(production)
            db.session.commit()
        else:
            print(f"No production found user id: {delete_id}")


# update
def update_inventory_production(update_id, name, new_inventory_quantity=None):
    with app.app_context():
        production = Inventory.query.filter_by(user_id=update_id, name=name).first()
        if production:
            # if new_type:
            #     production.type = new_type
            # if new_amount:
            #     production.amount = new_amount
            if new_inventory_quantity:
                production.InventoryQuantity = new_inventory_quantity
            db.session.commit()
        else:
            print(f"No production found with user id: {update_id}")
            
def update_inventory_production_demand_quantity(pid, item_name, demand_amount, user_id):
    with app.app_context():
        production2 = Inventory.query.filter_by(pid=pid, name=item_name, user_id=user_id).first()
        if production2:
            production2.DemandQuantity = demand_amount
            db.session.commit()

# update
def query_inventory_production(query_user_id, query_name):
    with app.app_context():
        production = Inventory.query.filter_by(user_id=query_user_id, name=query_name).first()
        if production:
            return production.pid, production.InventoryQuantity, production.DemandQuantity
        else:
            print(f"No production found with user id: {query_user_id}")
            return None


def add_delivery(name, sc_address, source_address, destination, send_time, receive_time, productId, quantities):
    with app.app_context():
        # existing_delivery = Delivery.query.filter_by(id=id).first()
        # if existing_delivery is None:
        new_delivery = Delivery(name=name, sc_address=sc_address, SourceAddress=source_address, Destination=destination, SendTime=send_time, ReceiveTime=receive_time, ProductId=productId, Quantities=quantities)
        db.session.add(new_delivery)
        db.session.commit()
        # else:
        #     print(f"Delivery with id {id} already exists.")


# update
def delete_delivery(product_id, sc_address, destination, send_time):
    with app.app_context():
        # substring = product_id
        # Delivery_filter = Delivery.query.filter_by(sc_address=sc_address, destination=destination, send_time=send_time).all()
        # for ProductIds in Delivery_filter:
        #if substring in ProductIds:
        delivery = Delivery.query.filter_by(ProductId=product_id, sc_address=sc_address, Destination=destination, SendTime=send_time).first()
        if delivery:
            db.session.delete(delivery)
            db.session.commit()
        else:
            print(f"No delivery found")


def update_delivery(product_id, sc_address, destination, new_receive_time):
    with app.app_context():
        delivery = Delivery.query.filter_by(ProductId=product_id, sc_address=sc_address, Destination=destination).first()
        if new_receive_time:
            delivery.ReceiveTime = new_receive_time
            db.session.commit()
        else:
            print(f"No delivery found")


def query_delivery(name):
    with app.app_context():
        delivery = Delivery.query.filter_by(name=name).first()
        if delivery:
            return delivery.sc_address, delivery.SourceAddress, delivery.Destination, delivery.ProductId, delivery.Quantities, delivery.ReceiveTime, delivery.id
        else:
            print(f"No delivery found")
            return None


def query_delivery_id(delivery_id):
    with app.app_context():
        delivery = Delivery.query.filter_by(id=delivery_id,
                                            ).first()
        if delivery:
                return delivery.SourceAddress, delivery.Destination, delivery.ProductId, delivery.Quantities, delivery.ReceiveTime, delivery.SendTime
        else:
                print(f"No delivery found")
                return None


def query_delivery_track(product_id, SourceAddress, Destination, Senddate):
    with app.app_context():
        delivery = Delivery.query.filter_by(ProductId=product_id,
                                            SourceAddress=SourceAddress,
                                            Destination=Destination, 
                                            SendTime=Senddate
                                            ).first()
        if delivery:
                return delivery.sc_address, delivery.SourceAddress, delivery.Destination, delivery.ProductId, delivery.Quantities, delivery.ReceiveTime, delivery.SendTime
        else:
                print(f"No delivery found")
                return None


def query_delivery_SD_pid(product_id, SourceAddress, SendTime):
    with app.app_context():
        delivery = Delivery.query.filter_by(ProductId=product_id,
                                            SourceAddress=SourceAddress,
                                            SendTime=SendTime
                                            ).first()
        if delivery:
                return delivery.sc_address, delivery.SourceAddress, delivery.Destination, delivery.ProductId, delivery.Quantities, delivery.ReceiveTime
        else:
                print(f"No delivery found")
                return None


def query_delivery_DT_pid(product_id, Destination, quantity):
    with app.app_context():
        delivery = Delivery.query.filter_by(ProductId=product_id,
                                            Destination=Destination, 
                                            Quantities=quantity
                                            ).first()
        if delivery:
            return delivery.sc_address, delivery.SourceAddress, delivery.Destination, delivery.ProductId, delivery.Quantities, delivery.ReceiveTime
        else:
            print(f"No delivery found")
            return None


# add items
def add_items(product_id, produce_time, deliveryIDs):
    with app.app_context():
        # existing_items = Items.query.filter_by(product_id=product_id).first()
        # if existing_items is None:
            new_items = Items(product_id=product_id, ProduceTime=produce_time, DeliveryIds=deliveryIDs)
            db.session.add(new_items)
            db.session.commit()
        # else:
        #     print(f"items with pid {product_id} already exists.")


def delete_items(product_id, produce_time):
    with app.app_context():
        item = Items.query.filter_by(product_id=product_id, ProduceTime=produce_time).first()
        if item:
            db.session.delete(item)
            db.session.commit()
        else:
            print(f"No item found with productID: {product_id}")


def update_item(product_id, produce_time, new_deliveryIDs=None):
    with app.app_context():
        item = Items.query.filter_by(product_id=product_id, ProduceTime=produce_time).first()
        if item:
            if new_deliveryIDs:
                item.DeliveryIds = new_deliveryIDs
            db.session.commit()
        else:
            print(f"No delivery found with id: {product_id}")


def query_item(product_id, produce_time):
    with app.app_context():
        item = Items.query.filter_by(product_id=product_id, ProduceTime=produce_time).first()
        if item:
            return item.id, item.ProduceTime, item.DeliveryIds
        else:
            print(f"No item found with productID: {product_id}")
            return None


# update
def add_contract_ABI(contract_name, SC_ABI):
    with app.app_context():
        existing_contract = contract_ABI.query.filter_by(contract_name=contract_name).first()
        if existing_contract is None:
            new_contract = contract_ABI(contract_name=contract_name, SC_ABI=SC_ABI)
            db.session.add(new_contract)
            db.session.commit()
        else:
            print(f"contract with contract_name {contract_name} already exists.")


def delete_contract(contract_name):
    with app.app_context():
        contract = contract_ABI.query.filter_by(contract_name=contract_name).first()
        if contract:
            db.session.delete(contract)
            db.session.commit()
        else:
            print(f"No contract found with contract_name: {contract_name}")


def update_contract(contract_name, new_SC_ABI=None):
    with app.app_context():
        contract = contract_ABI.query.filter_by(contract_name=contract_name).first()
        if contract:
            if new_SC_ABI:
                contract.SC_ABI = new_SC_ABI
            # if new_quantity:
            #     delivery.quantity = new_quantity
            # if new_destination:
            #     delivery.destination = new_destination
            db.session.commit()
        else:
            print(f"No contract found with contract_name: {contract_name}")


def query_contract(contract_name):
    with app.app_context():
        contract = contract_ABI.query.filter_by(contract_name=contract_name).first()
        if contract:
            return contract.contract_name, contract.SC_ABI
        else:
            print(f"No contract found with contract_name: {contract_name}")
            return None


if __name__ == '__main__':
    add_user('john', 'ammin', 'john.doe@example.com1', 'test12345', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db292', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db292')
    add_user('john2', 'ammin2', 'john.doe@example.com2', 'test12346', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db293', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db294')
    add_user('john3', 'ammin3', 'john.doe@example.com3', 'test12347', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db294', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db294')
    print(query_user_name('john'))
    print(query_user_email('john.doe@example.com1'))
    delete_token('fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db292')
    print(query_token_with_email('john.doe@example.com1'))
    update_user('john', new_type='manager', new_email='test@gmail.com')
    print(query_user_name('john'))
    print(query_user_email('test@gmail.com'))
    # delete_user('test@gmail.com')
    # print(query_user_name('john'))
    print(query_user_email('test@gmail.com'))
    print('\n\n')

    # add product and foreign key
    with app.app_context():
        # find the first user with the email 'john.doe@example.com2' in the User table
        user = User.query.filter_by(email='john.doe@example.com2').first()
        if user:
            add_product(user.id, 'VB', 'medicine')

    with app.app_context():
        # find the first user with the email 'john.doe@example.com2' in the User table
        user = User.query.filter_by(email='john.doe@example.com2').first()
        if user:
            add_product(user.id, 'Eyedrop', 'medicine')

    print(query_product('VB'))
    update_product('VB', new_type='medical equipment')
    print(query_product('VB'))

    # list Item Names
    print(query_product_user_id('john.doe@example.com2'))

    # with app.app_context():
    #     ItemNames = Product.query.filter(Product.user_id == 2).all()
    #     # for ItemName in ItemNames:
    #     #     print(ItemName.name)
    #     ItemName = [ItemName.name for ItemName in ItemNames]
    #     print(type(ItemName))
    #     print(ItemName)



    # delete_product('VB')
    # print(query_product('VB'))

    # use foreign key
    with app.app_context():
        child = Product.query.first()
        print(f"Child: {child.id}, Parent: {child.ProductOwner.name}")
    print('\n\n')

    # add inventory and foreign key
    with app.app_context():
        user = User.query.filter_by(email='john.doe@example.com2').first()
        product = Product.query.filter_by(name='VB', type='medicine').first()
        if user and product:
            add_inventory(user.id, product.id, 'inventory1', '123', '999')
    print(query_inventory_production('1', 'inventory1'))
    update_inventory_production('1', 'inventory1', '999999999')
    print(query_inventory_production('1', 'inventory1'))
    # delete_inventory_production('2', 'inventory1')
    # print(query_inventory_production('2','inventory1'))
    # use foreign key
    with app.app_context():
        child = Inventory.query.first()
        print(f"Child: {child.id}, Parent: {child.InventoryOwner.name}")
    print('\n\n')


    add_delivery('delivery1', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a558ab101c52db29232265', 'paradise1', 'paradise2', '07112023', '10112023', '123', '55, 66, 77')
    # print(query_delivery('delivery1'))
    # test=Delivery.ProductId
    # print(test)
    # print(query_delivery_id('1'))
    print(query_delivery_SD_pid('123', 'paradise1'))
    print(query_delivery_DT_pid('123', 'paradise2'))
    update_delivery('123', 'paradise1', 'paradise2', '07112023', '16112023')
    print(query_delivery('delivery1'))
    # print(query_delivery_id('1'))
    print(query_delivery_SD_pid('123', 'paradise1'))
    print(query_delivery_DT_pid('123', 'paradise2'))
    # delete_delivery('123', 'paradise1', 'paradise2', '07112023')
    # print(query_delivery_id('1'))
    print('\n\n')

    # update add items and foreign key
    with app.app_context():
        item = Product.query.filter_by(user_id=2, name='VB', type='medical equipment').first()
        if item:
            add_items(item.id, '08112023', '111, 222, 333')
    print(query_item('1', '08112023'))
    update_item('1', '08112023', '444, 555, 666')
    print(query_item('1', '08112023'))
    # delete_items('1', '08112023')
    # print(query_item('1', '08112023'))
    # use foreign key
    with app.app_context():
        child = Items.query.first()
        print(f"Child: {child.id}, Parent: {child.Items2Product.id}")
    print('\n\n')

    add_contract_ABI('Warehouse', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232261')
    print(query_contract('Warehouse'))
    add_contract_ABI('Producer', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232262')
    print(query_contract('Producer'))
    add_contract_ABI('Deployer', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232263')
    print(query_contract('Deployer'))
    add_contract_ABI('Delivery', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232264')
    print(query_contract('Delivery'))
    update_contract('Warehouse', 'fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232265')
    print(query_contract('Warehouse'))
    # delete_contract('Warehouse')
    # print(query_contract('Warehouse'))
    print('\n\n')