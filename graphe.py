import networkx as nx
import plotly.graph_objects as go
import pymysql

def connectToDb():
    connection = pymysql.connect('localhost','###','###',db='###')
    return connection

def closeDb(db):
    db.close()

def getUsers(db):
    with db.cursor() as cursor:
        sql = "SELECT idUsers, screenName FROM work.users where idUsers in (SELECT fkFollowingThisUsers FROM work.following WHERE fkIdUsers < 10 + 7484);"
        cursor.execute (sql)
        db.commit()
        result = cursor.fetchall()
        return result

def getEdge(db):
    with db.cursor() as cursor:
        sql = "SELECT fkIdUsers, fkFollowingThisUsers FROM work.following WHERE fkIdUsers IN (SELECT idUsers FROM work.users WHERE idUsers < 10 + 7484);"
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
        return result

db = connectToDb()
users = getUsers(db)

G = nx.Graph()

for user in users:
    G.add_node(user[0],name = user[1])

edges = getEdge(db)
for edge in edges:
    G.add_edge(edge[0],edge[1])

#G = nx.random_geometric_graph(200, 0.125)
edge_x = []
edge_y = []

pos = nx.spring_layout(G)
for node in G.nodes():
    G.nodes[node]['pos'] = pos[node]

for edge in G.edges():
    

    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']

    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)

    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines'
)

node_x = []
node_y = []

for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x = node_x,
    y = node_y,
    mode = 'markers+text',
    hoverinfo = 'text',
    name = 'text',
    textposition='top center',
    marker = dict(
        showscale = False,
        colorscale = 'YlGnBu',
        reversescale = True,
        color = [],
        size = 10,
        colorbar = dict(
            thickness = 15,
            title = 'Node Connections',
            xanchor = 'left',
            titleside = 'right'
        ),
        line_width = 2
    )
)

node_adjacencies = []
node_text = []
node_description = []
for node, adjacencies in enumerate(G.adjacency()):
    if len(adjacencies[1]) > 100:
        name = G.nodes[adjacencies[0]]['name']
    else:
        name = ''
    node_description.append(G.nodes[adjacencies[0]]['name'])
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append(name)
node_trace.marker.color = node_adjacencies
node_trace.text = node_text
node_trace.hovertext = node_description
fig = go.Figure(
    data = [edge_trace, node_trace],
    layout = go.Layout(
        showlegend = False,
        hovermode = 'closest',
        xaxis = dict(showgrid = False, zeroline = False, showticklabels = False),
        yaxis = dict(showgrid = False, zeroline = False, showticklabels = False)
        #geo = dict(bgcolor = 'rgba(1,1,1,0)')
    )
)

fig.update_layout(
    autosize = True,
    margin = dict(l = 0, r = 0, t = 0, b = 0)
)
fig.show()

