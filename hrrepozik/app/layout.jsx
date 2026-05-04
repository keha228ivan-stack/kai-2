import "./globals.css";

export const metadata = {
  title: "HR Web",
  description: "Manager panel",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
