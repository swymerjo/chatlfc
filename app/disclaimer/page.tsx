function Disclaimer() {
  return (
    <footer>
      <p className="box disclaimer" tabIndex={0}>
        This statbot provides information about results and goal contributions
        for LFC from the 2023/24 season. The app is a WIP and more data is being
        added daily.
      </p>
      <a
        href="https://www.buymeacoffee.com/statlfc"
        target="_blank"
        className="link"
      >
        Buy me a coffee/beer 🍺
      </a>
      <p className="copyright-text" tabIndex={0}>
        Copyright &copy; 2024
      </p>
    </footer>
  );
}

export default Disclaimer;
