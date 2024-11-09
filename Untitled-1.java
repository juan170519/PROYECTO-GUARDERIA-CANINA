import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.*;

public class Main extends JFrame {
    // Campos para la interfaz gráfica
    private JTextField txtNombre;
    private JCheckBox chkActivo;
    private JTextField txtEdad;
    private JTextField txtSalario;
    private JTextField txtInicial;
    private JTextArea txtAreaDatos;

    // Constructor para configurar la GUI
    public Main() {
        setTitle("Gestión de Datos");
        setSize(500, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 10, 10, 10);
        gbc.anchor = GridBagConstraints.WEST;

        // Crear y añadir campos a la ventana
        txtNombre = new JTextField(20);
        chkActivo = new JCheckBox();
        txtEdad = new JTextField(5);
        txtSalario = new JTextField(10);
        txtInicial = new JTextField(2);
        txtAreaDatos = new JTextArea(10, 40);
        txtAreaDatos.setEditable(false);
        txtAreaDatos.setLineWrap(true);
        txtAreaDatos.setWrapStyleWord(true);

        JScrollPane scrollPane = new JScrollPane(txtAreaDatos);
        scrollPane.setBorder(BorderFactory.createTitledBorder("Datos"));

        // Añadir componentes con GridBagConstraints
        addComponent(new JLabel("Nombre:"), 0, 0, gbc);
        addComponent(txtNombre, 1, 0, gbc);
        addComponent(new JLabel("Activo:"), 0, 1, gbc);
        addComponent(chkActivo, 1, 1, gbc);
        addComponent(new JLabel("Edad:"), 0, 2, gbc);
        addComponent(txtEdad, 1, 2, gbc);
        addComponent(new JLabel("Salario:"), 0, 3, gbc);
        addComponent(txtSalario, 1, 3, gbc);
        addComponent(new JLabel("Inicial:"), 0, 4, gbc);
        addComponent(txtInicial, 1, 4, gbc);
        
        JButton btnCargarDatos = new JButton("Cargar Datos");
        addComponent(btnCargarDatos, 0, 5, gbc, 2, 1);

        add(scrollPane, 0, 6, gbc, 2, 1);

        // Acción al pulsar el botón
        btnCargarDatos.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                cargarDatos();
            }
        });
    }

    private void addComponent(Component component, int x, int y, GridBagConstraints gbc) {
        addComponent(component, x, y, gbc, 1, 1);
    }

    private void addComponent(Component component, int x, int y, GridBagConstraints gbc, int width, int height) {
        gbc.gridx = x;
        gbc.gridy = y;
        gbc.gridwidth = width;
        gbc.gridheight = height;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        add(component, gbc);
    }

    // Método para conectar a la base de datos y cargar datos
    private void cargarDatos() {
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            // Conectar a la base de datos
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/mydb", "root", "");

            // Ejecutar la consulta
            String query = "SELECT * FROM my_table";
            stmt = conn.createStatement();
            rs = stmt.executeQuery(query);
            StringBuilder datos = new StringBuilder();

            // Procesar los resultados
            while (rs.next()) {
                String nombre = rs.getString("nombre");
                boolean esActivo = rs.getBoolean("esActivo");
                int edad = rs.getInt("edad");
                float salario = rs.getFloat("salario");
                char inicial = rs.getString("inicial").charAt(0);

                datos.append("Nombre: ").append(nombre)
                      .append(", Activo: ").append(esActivo)
                      .append(", Edad: ").append(edad)
                      .append(", Salario: ").append(salario)
                      .append(", Inicial: ").append(inicial).append("\n");
            }

            // Mostrar los datos en el área de texto
            txtAreaDatos.setText(datos.toString());
        } catch (SQLException ex) {
            JOptionPane.showMessageDialog(this, "Error al cargar datos: " + ex.getMessage());
        } finally {
            // Cerrar recursos
            try {
                if (rs != null) rs.close();
                if (stmt != null) stmt.close();
                if (conn != null) conn.close();
            } catch (SQLException ex) {
                ex.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        // Configurar y mostrar la interfaz gráfica
        SwingUtilities.invokeLater(() -> {
            Main main = new Main();
            main.setVisible(true);
        });
    }
}