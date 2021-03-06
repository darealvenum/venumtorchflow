import numpy as np


class Loss:
    """ base class for loss functions """

    def calculate(self, output, y, *, include_regularization=False):
        """ 
        calculate the loss for a batch

        parameters:
        -----------

        output: np.array
            the output of the network for a batch
        y: np.array
            the labels of the batch
        include_regularization: bool
            whether or not to include the regularization loss in the total loss
        """
        sample_losses = self.forward(output, y)

        self.accumulated_sum += np.sum(sample_losses)
        self.accumulated_count += len(sample_losses)

        # gemiddelde loss
        data_loss = np.mean(sample_losses)
        if not include_regularization:
            return data_loss

        return data_loss, self.regularization_loss()

    def remember_trainable_layers(self, trainable_layers):
        """
        remeber which layers are trainable

        parameters:
        ----------
        trainable_layers: list[nn.layer()]
            the layers that are trainable
        """
        self.trainable_layers = trainable_layers

    def regularization_loss(self):
        # 0 default
        regularization_loss = 0

        for layer in self.trainable_layers:
            # L1 en L2 Regularization weights
            if layer.weight_regularizer_l1 > 0:
                regularization_loss += layer.weight_regularizer_l1 * \
                    np.sum(np.abs(layer.weights))

            if layer.weight_regularizer_l2 > 0:
                regularization_loss += layer.weight_regularizer_l2 * \
                    np.sum(layer.weights * layer.weights)

            # L1 en L2 Regularization biases
            if layer.bias_regularizer_l1 > 0:
                regularization_loss += layer.bias_regularizer_l1 * \
                    np.sum(np.abs(layer.biases))

            if layer.bias_regularizer_l2 > 0:
                regularization_loss += layer.bias_regularizer_l2 * \
                    np.sum(layer.biases * layer.biases)

        return regularization_loss

    def calculate_accumulated(self, *, include_regularization=False):
        """ 
        calculate the accumulated loss

        parameters
        ----------
        include_regularization: bool
            whether or not to include the regularization loss in the total loss
        """

        # bereken de loss van een batch
        data_loss = self.accumulated_sum / self.accumulated_count

        if not include_regularization:
            return data_loss

        return data_loss, self.regularization_loss()

    def new_pass(self):
        # reset alle holders
        self.accumulated_sum = 0
        self.accumulated_count = 0
