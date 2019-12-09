from flask import Flask, render_template, request, jsonify
import pusher

# Create Flask app
app = Flask(__name__)

# Configure Pusher objects
pusher_client = pusher.Pusher(
  app_id='796659',
  key='25860c8518b767230f19',
  secret='a42b559d5ef4c44b9f4b',
  cluster='eu',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

# Index route, index.html view
@app.route('/')
def index():
  return render_template('index.html')

# Endpoint for storing to-do item
@app.route('add-todo', methods = ['POST'])
def addTodo():
  # loads json data from request
  data = json.loads(request.data)
  # trigger item-added event on to-do channel
  pusher.trigger('todo', 'item-added', data)
  return jsonify(data)

# Endpoint for deleting to-do data
@app.route('/remove-todo/<item_id>')
def removeTodo(item_id):
  data = {'id': item_id}
  pusher.trigger('todo', 'item-removed', data)
  return jsonify(data)

# Endpoint for updating to-do data
@app.route('/update-todo/<item_id>', methods = ['POST'])
def updateTodo(item_id):
  data = {
    'id': item_id,
    'completed': json.loads(request.data).get('completed', 0)
  }
  pusher.trigger('todo', 'item-updated', data)
  return jsonify(data)
