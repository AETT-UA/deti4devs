export default function BaseLayout({ children }) {
  return (
    <>
      <Navbar />
      {children}
    </>
  );
}
