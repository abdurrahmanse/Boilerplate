import { Toolbar as BasehubToolbar } from "basehub/next-toolbar";
import { keys } from "../keys";

export const Toolbar = () => {
  const { BASEHUB_TOKEN } = keys();
  if (!BASEHUB_TOKEN) return null;
  return <BasehubToolbar />;
};
