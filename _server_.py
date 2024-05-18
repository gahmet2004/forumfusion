import _main_ as ForumFusion

from waitress import serve

serve(
    ForumFusion,
    host = "0.0.0.0",
    port = "80"
)
