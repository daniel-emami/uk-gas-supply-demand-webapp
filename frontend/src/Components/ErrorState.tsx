interface ErrorStateProps {
  message: string;
}

export default function ErrorState({ message }: ErrorStateProps) {
  return (
    <div className="state-card error-card">
      <strong>Could not load gas flow data.</strong>
      <span>{message}</span>
    </div>
  );
}
