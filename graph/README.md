# graph/

Relationship data that powers the Research Graph visualization.

## Why a graph

The 115-leader list is a set of nodes. The connections between them — who advised whom, who co-founded with whom, who came out of which lab — tell stories the list alone cannot. Click on Jennifer Doudna and see Rachel Haurwitz spin out from her lab. Click on Fei-Fei Li and see her network of advisees now at other major institutions. Click on any leader in India and see the IIT → Stanford pipeline rendered visually.

The graph view is planned for v1.1. This folder will contain the generated artifacts that power it.

## Structure

When the graph build script ships, this folder will contain:

- `nodes.json` — every leader as a node, with tier, domain, origin, and metadata for styling
- `edges.json` — every relationship between leaders, with type, context, and source
- `exports/` — same data exported in standard graph formats (GraphML, GEXF for Gephi, D3 JSON)

## How it's built

The graph is derived, not primary. The source of truth remains `data/leaders/*.yaml`. A build script (`scripts/build_graph.py`, planned) reads the `relationships` fields across all leader files and produces the JSON artifacts in this folder.

Running the build is idempotent: given the same `data/`, it always produces the same graph.

## Contributing relationships

To add a relationship, edit the relevant leader YAML and add to its `relationships` list. The build script regenerates this folder automatically. See [`CONTRIBUTING.md`](../CONTRIBUTING.md#how-to-add-relationships) for the relationship schema.

Relationships are symmetric. If you add Leader A as advisor to Leader B, also add Leader B as advisee to Leader A. The validation script flags missing reciprocals.

## Planned graph views

For v1.1, the site at `/graph`:

- Force-directed layout with nodes colored by domain
- Click a node to focus on its ego-network
- Filters for tier, origin (India / rest-of-world), and domain
- Search for a specific leader to center the graph on them
- A "share this view" URL that captures filters and focal node

Tooling decision (tentative): [Cosmograph](https://cosmograph.app/) for the browser rendering if the graph stays under ~10K nodes (it will for the foreseeable future). Fallback to D3-force if we need something more customizable.

## Scale considerations

At v1.0 (115 leaders), the graph may have 200-500 edges. At v1.3 (targeting 300 leaders), it may have 1000-2000 edges. These are small graphs; performance will not be a constraint until the dataset scales significantly.

If the Index later expands beyond frontier women to adjacent verticals (e.g., frontier climate leaders), we may split graphs by vertical and offer cross-vertical views.
