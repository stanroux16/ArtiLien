export function Champ(props: {
  nom: string; libelle: string; type?: string; erreur?: string; aide?: string; autoComplete?: string;
}) {
  const { nom, libelle, type = "text", erreur, aide, autoComplete } = props;
  return (
    <div className="flex flex-col gap-1">
      <label htmlFor={nom} className="font-medium">{libelle}</label>
      <input
        id={nom} name={nom} type={type} autoComplete={autoComplete} required
        aria-invalid={!!erreur} aria-describedby={erreur ? `${nom}-err` : undefined}
        className="min-h-12 rounded-champ border border-bordure bg-surface px-4 text-texte"
      />
      {aide && <span className="text-sm text-secondaire">{aide}</span>}
      {erreur && <span id={`${nom}-err`} role="alert" className="text-sm text-erreur">{erreur}</span>}
    </div>
  );
}
