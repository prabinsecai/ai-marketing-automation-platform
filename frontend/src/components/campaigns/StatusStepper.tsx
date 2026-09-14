import React from "react";
import { Check, Clock, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { CampaignStatusType } from "@/lib/types";

interface StatusStepperProps {
  currentStatus: CampaignStatusType;
}

const steps = [
  { key: "DRAFT", label: "Draft" },
  { key: "STRATEGY_GENERATED", label: "Strategy" },
  { key: "CONTENT_GENERATED", label: "Content" },
  { key: "IN_REVIEW", label: "In Review" },
  { key: "APPROVED", label: "Approved" },
];

export const StatusStepper: React.FC<StatusStepperProps> = ({ currentStatus }) => {
  const currentIndex = steps.findIndex((s) => s.key === currentStatus);

  return (
    <div className="w-full bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-4 shadow-sm">
      <div className="flex items-center justify-between overflow-x-auto">
        {steps.map((step, idx) => {
          const isPassed = idx < currentIndex;
          const isCurrent = idx === currentIndex;
          const isPending = idx > currentIndex;

          return (
            <React.Fragment key={step.key}>
              <div className="flex items-center gap-2.5 shrink-0">
                <div
                  className={cn(
                    "w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold transition-all",
                    isPassed && "bg-emerald-500 text-white",
                    isCurrent && "bg-indigo-600 text-white ring-4 ring-indigo-500/20",
                    isPending && "bg-zinc-100 dark:bg-zinc-800 text-zinc-400 border border-zinc-200 dark:border-zinc-700"
                  )}
                >
                  {isPassed ? (
                    <Check className="w-4 h-4 stroke-[2.5]" />
                  ) : isCurrent ? (
                    <Clock className="w-3.5 h-3.5" />
                  ) : (
                    idx + 1
                  )}
                </div>
                <div className="text-left">
                  <p
                    className={cn(
                      "text-xs font-semibold",
                      isCurrent
                        ? "text-indigo-600 dark:text-indigo-400"
                        : isPassed
                        ? "text-zinc-800 dark:text-zinc-200"
                        : "text-zinc-400"
                    )}
                  >
                    {step.label}
                  </p>
                  <p className="text-[10px] text-zinc-400">
                    {isCurrent ? "Active Stage" : isPassed ? "Completed" : "Upcoming"}
                  </p>
                </div>
              </div>

              {idx < steps.length - 1 && (
                <ChevronRight className="w-4 h-4 text-zinc-300 dark:text-zinc-700 mx-2 shrink-0" />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
