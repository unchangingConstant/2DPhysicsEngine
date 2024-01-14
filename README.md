# 2DPhysicsEngine
A program that handles physics for a 2D environment. For now, it can handle interactions between a moving dot and immovable edges.

True position branch addresses an issue that came from resolving the first issue on this project - since the field methods for entity only allow whole numbers to come through, whenever elasticity is applied to a bounce, the amount of velocity a ball loses per bounce is not accurately represented. Example: Elasticity of 0.9 means that when the ball bounces on surface, its velocity will only be 0.9 of what it was from before it bounced. With the new mutator/setter methods, an elasticity of .9 and .99 will virtually work the same.

I will address this by rounding to a nearest decimal as opposed to a whole number in the entity's field methods. To how many decimal places? That is a completely arbitrary decision. So I will choose: 5 decimal places.
