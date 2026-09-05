import { useI18n } from "../i18n/I18nProvider";
import "./StoreView.css";

export default function StoreView() {
  const { t } = useI18n();

  const categories = [
    { key: "shopping", icon: "🛒" },
    { key: "deals", icon: "🏷" },
    { key: "compare", icon: "📊" },
    { key: "community", icon: "🤝" },
  ];

  return (
    <div className="store-view">
      <div className="store-hero">
        <div className="store-icon">🛍</div>
        <h1 className="store-title">{t("store.title")}</h1>
        <p className="store-desc">{t("store.description")}</p>
        <span className="store-soon">{t("store.comingSoon")}</span>
      </div>

      <div className="store-cats">
        {categories.map((c) => (
          <div key={c.key} className="store-cat">
            <span className="store-cat-icon">{c.icon}</span>
            <span className="store-cat-label">{t(`store.cats.${c.key}`)}</span>
            <span className="store-cat-soon">{t("common.comingSoon")}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
