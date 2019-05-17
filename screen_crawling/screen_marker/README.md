## Good selectors for sites

## Train data


### Amazon

url = `https://www.amazon.com/`

class = `a-row dealContainer dealTile`

### Rozetka

url = `https://www.citrus.ua/`

class = `main-goods__cell`

### Citrus

url = `https://www.citrus.ua/`

### Foxtrot

## Test data


### rost

url = `https://rost.kh.ua/`

class = `item`










```

input_image = Input(shape=(320, 200, 4))

conv_1 = Conv2D(126, (3, 3), padding='same', activation='relu')(input_image)
batch_1 = BatchNormalization()(conv_1)
conv_2 = Conv2D(126, (3, 3), padding='same', activation='relu')(batch_1)
batch_2 = BatchNormalization()(conv_2)

max_pooling_2 = MaxPooling2D(pool_size=(4, 4))(batch_2)

conv_1_2 = Conv2D(64, (3, 3), padding='same', activation='relu')(max_pooling_2)
batch_1_2 = BatchNormalization()(conv_1_2)
conv_2_2 = Conv2D(64, (3, 3), padding='same', activation='relu')(batch_1_2)
batch_2_2 = BatchNormalization()(conv_2_2)

up_sampling_3 = UpSampling2D((4, 4))(batch_2_2)

conv_3_1 = Conv2D(16, (3, 3), padding='same', activation='relu')(up_sampling_3)
conv_3_2 = Conv2D(16, (3, 3), padding='same', activation='relu')(conv_3_1)

out = Conv2D(4, (3, 3), padding='same', activation='softmax')(conv_3_2)

model = Model(input_image, out)
model.summary()

```

```
#opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6) #keras.optimizers.Adam(lr=0.0002, beta_1=0.5)
opt = keras.optimizers.Adam(lr=0.0002, decay=1e-6)
# Let's train the model using RMSprop № categorical_crossentropy
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])
```

```
model.fit(x_train, y_train,
          batch_size=10,
          epochs=10,
          shuffle=True)
```