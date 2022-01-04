# Numerai Blocks
> Tools for solid Numerai pipelines


```
%load_ext autoreload
%autoreload 2
```

## Install

`pip install numerai-blocks`

## How to use

Development notebooks are in the `nbs` directory. Example and educational notebooks can be found in the `edu_nbs` directory.

- Downloaders
- Dataloaders
- Dataset objects (with arbitrary metadata)
- Preprocessing
- Model
- ModelPipeline and ModelPipelineCollection (Or FeatureUnion??)
- Postprocessing
- Prediction dataset (with arbitrary metadata)
- Evaluators
- Key (containing authentication info)
- Submittors

```
1+1
```




    2



```
import uuid
print(uuid.uuid4())
```

    649ce02a-6fb4-4b1f-8375-d3b46ed391c9


## Contributing

After you clone this repository, please run `nbdev_install_git_hooks` in your terminal. This sets up git hooks, which clean up the notebooks to remove the extraneous stuff stored in the notebooks (e.g. which cells you ran) which causes unnecessary merge conflicts.

### Branch structure



<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">Brranch structure                                                                                   
<span style="color: #808080; text-decoration-color: #808080">┗━━ </span>📦 main (release)                                                                               
<span style="color: #808080; text-decoration-color: #808080">    ┗━━ </span>👨‍💻 dev                                                                                    
<span style="color: #808080; text-decoration-color: #808080">        ┣━━ </span>✨ feature/1                                                                            
<span style="color: #808080; text-decoration-color: #808080">        ┣━━ </span>✨ feature/2                                                                            
<span style="color: #808080; text-decoration-color: #808080">        ┗━━ </span>✨ feature/3                                                                            
</pre>


