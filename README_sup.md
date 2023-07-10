## 运行环境
根据作者提供的readme进行配置(注意依赖包版本), 可以直接用我配好的虚拟环境:
~~~shell
conda activate /mnt/cephfs/mixed/home/alvin/envs/yangzh-open-mmlab
~~~
## 准备数据集
要在项目根目录下新建一个data文件夹存放数据, 数据集可以放在其他地方比如公共目录下, 然后建一个软链接连过去就可以:
~~~shell
ln -s /mnt/cephfs/dataset/imagenet data/imagenet
~~~
## 模型划分 & 集成
1. 完整的流程需要先计算出模型之间的表征相似度, 目前是直接利用作者提供的预先计算好的值, 需要先下载下来:
Pre-computed similarity on ImageNet for [Linear CKA](https://drive.google.com/drive/folders/1ebSVwZyKeHdmdOdVlFZF6P9_1PzEMs-J?usp=share_link)
2. 接下来是步骤根据作者提供的readme来就可以, 注意要根据你所要集成的模型修改block_meta.py中的MODEL_ZOO
3. 最终会生成一个resaemly文件，其实就是一个集成模型的配置
## fine-tuning
1. 首先要配置好训练用的config, 根据你要用到的数据集和训练的模型配置好datasets, schedules和model
2. 最后运行命令:
~~~shell
bash tools/dist_train.sh [config_path] [nums_gpu]
~~~
