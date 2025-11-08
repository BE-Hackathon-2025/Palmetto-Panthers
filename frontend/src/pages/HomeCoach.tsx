import { useState, useEffect } from "react";
import { ChatInterface } from "@/components/ChatInterface";
import { ReadinessCard } from "@/components/ReadinessCard";
import { TimelineCard } from "@/components/TimelineCard";
import { DPAMatchCard } from "@/components/DPAMatchCard";
import { DocumentUploadCard } from "@/components/DocumentUploadCard";
import { CreditTuneUpCard } from "@/components/CreditTuneUpCard";
import { LenderPacketCard } from "@/components/LenderPacketCard";
import { PreApprovalCard } from "@/components/PreApprovalCard";
import { AppraisalPrepCard } from "@/components/AppraisalPrepCard";
import { CompletionSurveyCard } from "@/components/CompletionSurveyCard";
import { ChatMessage, ReadinessScore, UserProfile, DocumentItem } from "@/types/homebuyer";
import { calculateReadinessScore, generateTimeline } from "@/utils/calculations";
import { Card } from "@/components/ui/card";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { Shield, MessageCircle, PartyPopper } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

type Phase =
  | "initial"
  | "readiness"
  | "documents"
  | "credit"
  | "packet"
  | "preapproval"
  | "appraisal"
  | "survey"
  | "complete";

export default function HomeCoach() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [chatOpen, setChatOpen] = useState(true);
  const [userProfile, setUserProfile] = useState<Partial<UserProfile>>({});
  const [readiness, setReadiness] = useState<ReadinessScore | null>(null);
  const [currentPhase, setCurrentPhase] = useState<Phase>("initial");
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [completedPhases, setCompletedPhases] = useState<Set<string>>(new Set());

  // 🟢 Load user from localStorage (auth integration ready)
  useEffect(() => {
    const storedUser = localStorage.getItem("user_id");
    if (storedUser) {
      setUserProfile({ id: storedUser });
    } else {
      // fallback for demo/testing only
      const defaultId = "xenfzFaXTmWWwpbxQFw6hyUji8I2";
      setUserProfile({ id: defaultId });
      localStorage.setItem("user_id", defaultId);
    }
  }, []);

  // 🟢 Show welcome message on load
  useEffect(() => {
    setMessages([
      {
        id: "welcome",
        role: "assistant",
        content: `Hi, I'm Haven — your AI home coach! Let's begin your journey.`,
        timestamp: new Date().toISOString(),
      },
    ]);
  }, []);

  // 🧠 Main chat handler (connected to FastAPI backend)
  const handleSendMessage = async (content: string) => {
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userProfile.id,
          query: content,
        }),
      });

      if (!res.ok) throw new Error(`Backend error: ${res.status}`);

      const data = await res.json();

      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content:
          data.assistant_response ||
          "I'm here to help, but I couldn’t process that right now.",
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat API error:", error);
      setMessages((prev) => [
        ...prev,
        {
          id: `error-${Date.now()}`,
          role: "assistant",
          content: "⚠️ Sorry, I couldn’t connect to the server. Please try again.",
          timestamp: new Date().toISOString(),
        },
      ]);
    }
  };

  const milestones = readiness ? generateTimeline(readiness.eta_weeks) : [];

  // === Document & Phase Handlers ===
  const handleDocumentUpload = (type: string) => {
    setDocuments((prev) => [
      ...prev,
      { type, status: "verified" as const, uploaded_at: new Date().toISOString() },
    ]);
  };

  const handleDocumentsComplete = () => {
    setCompletedPhases((prev) => new Set(prev).add("documents"));
    setCurrentPhase("credit");
    toast.success("✅ Documents complete! Moving to credit tune-up phase.");
  };

  const handleCreditComplete = () => {
    setCompletedPhases((prev) => new Set(prev).add("credit"));
    setCurrentPhase("packet");
    toast.success("💪 Credit tuned up! Next: Lender packet.");
  };

  const handlePacketComplete = () => {
    setCompletedPhases((prev) => new Set(prev).add("packet"));
    setCurrentPhase("preapproval");
    toast.success("📄 Lender packet ready! Moving to pre-approval.");
  };

  const handlePreApprovalComplete = () => {
    setCompletedPhases((prev) => new Set(prev).add("preapproval"));
    setCurrentPhase("appraisal");
    toast.success("🏡 Great work! Appraisal prep next.");
  };

  const handleAppraisalComplete = () => {
    setCompletedPhases((prev) => new Set(prev).add("appraisal"));
    setCurrentPhase("survey");
    toast.success("🎉 Almost there! Final survey ahead.");
  };

  const handleSurveyComplete = () => {
    setCurrentPhase("complete");
    toast.success("Thank you for your feedback!");
  };

  // === Render ===
  return (
    <div className="min-h-screen flex flex-col bg-background">
      <div className="flex-1 overflow-hidden">
        <div className="h-full overflow-y-auto bg-muted/30 p-4 md:p-6">
          <div className="max-w-2xl mx-auto space-y-4 md:space-y-6 pb-20 md:pb-6">

            {/* Welcome Card */}
            {currentPhase === "initial" && (
              <Card className="p-6 md:p-8 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20 text-center">
                <h2 className="text-2xl md:text-3xl font-bold">Welcome to HomeReady! 👋</h2>
                <p className="text-base md:text-lg text-muted-foreground mt-2">
                  Let's start a conversation about your homebuying journey.
                </p>
                <Button
                  size="lg"
                  onClick={() => setChatOpen(true)}
                  className="mt-4 text-base md:text-lg"
                >
                  <MessageCircle className="mr-2 h-5 w-5" />
                  Start Chat
                </Button>
              </Card>
            )}

            {/* Privacy Notice */}
            <Card className="p-4 bg-accent/10 border-accent">
              <div className="flex items-start gap-3">
                <Shield className="h-5 w-5 text-accent shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-sm mb-1">Your Privacy Matters</h3>
                  <p className="text-xs text-muted-foreground">
                    All data encrypted. No credit pulls. You're in control.
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>

      {/* Floating Chat Drawer */}
      <Sheet open={chatOpen} onOpenChange={setChatOpen}>
        <SheetTrigger asChild>
          <Button
            size="lg"
            className="fixed bottom-4 right-4 md:bottom-6 md:right-6 h-14 w-14 rounded-full shadow-lg hover:scale-110 transition-transform z-50"
          >
            <MessageCircle className="h-6 w-6" />
          </Button>
        </SheetTrigger>

        <SheetContent side="left" className="w-full sm:w-[440px] md:w-[540px] p-0 flex flex-col">
          <SheetHeader className="px-4 md:px-6 py-3 md:py-4 border-b border-border">
            <SheetTitle className="text-left text-base md:text-lg">
              Haven - HomeReady Coach
            </SheetTitle>
          </SheetHeader>
          <div className="flex-1 overflow-hidden">
            <ChatInterface
              messages={messages}
              onSendMessage={handleSendMessage}
              isLoading={false}
            />
          </div>
        </SheetContent>
      </Sheet>
    </div>
  );
}