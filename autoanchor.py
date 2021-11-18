import utils.autoanchor as autoAC
 
# 对数据集重新计算 anchors
new_anchors = autoAC.kmean_anchors('./data/roco.yaml', 9, 640, 3.0, 1000, True)
print(new_anchors)
