from typing import Generator, Tuple

import numpy as np
import pandas as pd


class ExpandingWindowSplitter:
    """Generador de splits de tipo Expanding Window.

    Usado para validacion cruzada en series temporales.
    """

    def __init__(self, initial_train_size: int, step_size: int = 1):
        """Inicializa el splitter.

        Args:
            initial_train_size: Numero inicial de observaciones para el train.
            step_size: Tamanio del paso para expandir la ventana.
        """
        self.initial_train_size = initial_train_size
        self.step_size = step_size

    def split(
        self, df: pd.DataFrame
    ) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """Genera los indices de train y test iterativamente."""
        n_samples = len(df)
        if self.initial_train_size >= n_samples:
            raise ValueError("El tamanio inicial debe ser menor al numero de muestras.")

        current_train_end = self.initial_train_size

        while current_train_end < n_samples:
            train_idx = np.arange(0, current_train_end)
            test_end = min(current_train_end + self.step_size, n_samples)
            test_idx = np.arange(current_train_end, test_end)

            yield train_idx, test_idx

            current_train_end += self.step_size
