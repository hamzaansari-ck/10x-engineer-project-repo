export default function Layout({ header, sidebar, children }) {
  return (
    <div className="app-layout">
      {header}
      <div className="app-body">
        {sidebar}
        <main className="app-main">{children}</main>
      </div>
    </div>
  );
}
