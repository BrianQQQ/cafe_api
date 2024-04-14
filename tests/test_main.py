def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h1>Welcome to the Cafe & Wifi API</h1>' in response.data

def test_add(client):
    response = client.post('/add', data={
        'name': 'Test Cafe',
        'map_url': 'https://www.google.com/maps/place/1234',
        'img_url': 'https://www.example.com/image.jpg',
        'loc': 'Test Location',
        'sockets': True,
        'toilet': False,
        'wifi': True,
        'calls': False,
        'seats': 10,
        'coffee_price': 5.00
    })
    assert response.status_code == 200
    assert b'Successfully added the new cafe.' in response.data

def test_get_random(client):
    response = client.get('/random')
    assert response.status_code == 200
    assert b'"can_take_calls":true,"coffee_price":"5.0","has_sockets":true,"has_toilet":true,"has_wifi":true,"img_url":"https://www.example.com/image.jpg","location":"Test Location","map_url":"https://www.google.com/maps/place/1234","name":"Test Cafe","seats":"10"' in response.data

def test_get_all(client):
    response = client.get('/all')
    assert response.status_code == 200
    assert b'"can_take_calls":true,"coffee_price":"5.0","has_sockets":true,"has_toilet":true,"has_wifi":true,"img_url":"https://www.example.com/image.jpg","location":"Test Location","map_url":"https://www.google.com/maps/place/1234","name":"Test Cafe","seats":"10"' in response.data

def test_update_cafe(client):
    response = client.patch('/update-cafe/1?new_price=6.00')
    assert response.status_code == 200
    assert b'coffee_price":"6.00'
    assert b'Successfully updated the price.' in response.data

def test_delete_cafe(client):
    response = client.delete('/report-close/1?api_key=secret')
    assert response.status_code == 200
    assert b'Successfully reported cafe as closed.' in response.data