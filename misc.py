import pandas as pd
import matplotlib as plt

def rake_data_plotter():
    df = pd.read_csv(
        r'G:\01 - Aero Projects\06 - FS Data\Race & Test Data\2022\Documents\Rake csv files\WT\22W18\R109079_RW_Onset_rake_tunnel\6.2mmFRH  70mmRRH  0degYaw   0degStr    0degRoll     .csv')
    print(df)

    x, y, Cp = df.Y, df.Z, df.TotalPressureCoefficient

    # Set up a regular grid of interpolation points
    xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate
    rbf = scipy.interpolate.Rbf(x, y, Cp, function='linear')
    zi = rbf(xi, yi)

    # plt.contourf(x, y, zi)
    plt.imshow(zi, vmin=Cp.min(), vmax=Cp.max(), origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()])
    # plt.scatter(x, y, c=Cp)
    plt.colorbar()
    plt.show()