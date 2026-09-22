# Muwajjih

Muwajjih is my SDA-AIE-113 capstone project.

It receives a short complaint and returns:

- the correct department
- the priority: `normal` or `urgent`

The department is predicted using a small scikit-learn model.

Emergency words such as `fire` and `gas leak` are handled by a fixed rule, so they always return:

```text
priority = urgent